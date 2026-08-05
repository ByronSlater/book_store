# scp -r -i ~/.ssh/byron_cloud_deployment.pem ./* ec2-user@18.175.50.27:~/book_store

rsync -azvp --exclude={'node_modules', '*.pyi', '__pycache__'} --delete -e "ssh -i ~/.ssh/byron_cloud_deployment.pem" ./* ec2-user@18.175.50.27:~/book_store
