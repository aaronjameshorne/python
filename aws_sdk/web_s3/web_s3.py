import boto3
import click

session = boto3.Session(profile_name='default')
s3 = session.resource('s3')


@click.group()
def cli():
    "deploys websites to AWS"
    pass

@cli.command('list-buckets')
def list_buckets():
    "List all s3 buckets"
    for bucket in s3.buckets.all():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)
    
@cli.command('setup-bucket')
@cli.argument('bucket')
def setup_bucket(bucket):
    "Creat and config site"
    s3_bucket = s3.create_bucket(Bucket='ansible-aws-bucket-site',CreateBucketConfiguration={'LocationConstraint':session.region_name})
    policy = """
     {
      "Version":"2012-10-17",
      "Statement":[{
      "Sid":"PublicReadGetObject",
      "Effect":"Allow",
      "Principal": "*",
          "Action":["s3:GetObject"],
          "Resource":["arn:aws:s3:::%s/*"
        ]
      }
      ]
     }
      """
   policy = policy.strip()
   pol.put(Policy=policy)
   ws = new_bucket.Website()
   ws.put(WebsiteConfiguration={'ErrorDocument':{'Key':'error.html'},'IndexDocument':{'Suffix':'index.html'}})

if __name__ == '__main__':
    cli()
    
    

