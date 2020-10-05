add deployment service user permissions
```shell script
 gcloud iam service-accounts add-iam-policy-binding deployment@ana-shopping-bie.iam.gserviceaccount.com --member=serviceAccount:deployment@ana-shopping-bie.iam.gserviceaccount.com --role=roles/iam.serviceAccountUser
```

plan infra
```shell script 
 terraform plan -var-file=env.tfvars --out="output.txt"
```

deploy infra
```shell script 
 terraform apply "output.txt"
```

destroy infra
```shell script 
 terraform destroy -var-file=env.tfvars -auto-approve
```

generate function http trigger urls
```shell script
 terraform output -json > env.json
```
