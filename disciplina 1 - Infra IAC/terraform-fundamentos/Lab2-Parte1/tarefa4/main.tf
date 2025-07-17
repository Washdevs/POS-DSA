module "dsa_ec2_instances" {

source "./modules/ec2-instances"
  
  instance_count  = 2
  ami_id          = "ami-0eb9d6fc9fab44d24"
  instance_type   = "t2.micro"
  subnet_id       = "subnet-0263b2195d301ca3b"
}