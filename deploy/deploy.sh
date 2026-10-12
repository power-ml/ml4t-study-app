#!/bin/bash
# Deploy the study app to YOUR personal AWS account (private, login-protected). Run it on your PERSONAL
# computer with your own AWS CLI profile — never put personal cloud credentials on a work machine.
#   AWS_PROFILE=personal ./deploy/deploy.sh you@example.com            (re-run any time to push updates)
# Needs: AWS CLI v2, Python 3. Creates the CloudFormation stack "ml4t-study" in us-east-1.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${AWS_PROFILE:?Set AWS_PROFILE to your personal AWS CLI profile}"
EMAIL="${1:?usage: AWS_PROFILE=... ./deploy/deploy.sh you@example.com [cognito-domain-prefix]}"
PREFIX="${2:-ml4t-study-$(printf '%s' "$EMAIL$(aws sts get-caller-identity --query Account --output text)" | shasum | cut -c1-8)}"
STACK=ml4t-study; REGION=us-east-1
echo "Account: $(aws sts get-caller-identity --query Account --output text)  Region: $REGION  Stack: $STACK"
aws cloudformation deploy --region "$REGION" --stack-name "$STACK" --template-file deploy/ml4t-hosting.yaml \
  --capabilities CAPABILITY_IAM --parameter-overrides CognitoDomainPrefix="$PREFIX" --no-fail-on-empty-changeset
out() { aws cloudformation describe-stacks --region "$REGION" --stack-name "$STACK" --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text; }
BUCKET=$(out BucketName); DIST=$(out DistributionId); URL=$(out SiteUrl); POOL=$(out UserPoolId); CLIENT=$(out ClientId); DOMAIN=$(out CognitoDomain)
rm -rf deploy/build && python3 deploy/build_site.py --out deploy/build --domain "$DOMAIN" --client "$CLIENT"
aws s3 cp deploy/build "s3://$BUCKET/" --recursive --region "$REGION" --cache-control "no-cache"
aws cloudfront create-invalidation --distribution-id "$DIST" --paths '/*' --query Invalidation.Id --output text >/dev/null
if ! aws cognito-idp admin-get-user --region "$REGION" --user-pool-id "$POOL" --username "$EMAIL" >/dev/null 2>&1; then
  aws cognito-idp admin-create-user --region "$REGION" --user-pool-id "$POOL" --username "$EMAIL" \
    --user-attributes Name=email,Value="$EMAIL" Name=email_verified,Value=true --desired-delivery-mediums EMAIL >/dev/null
  echo "Created your login. A temporary password was emailed to $EMAIL (you'll set a new one at first sign-in)."
fi
echo "Done. Open: $URL   (first deploy: CloudFront can take ~5-15 minutes to come up)"
