variable "region" {
    description = "A região da AWS onde os recursos serão criados"
    type = string
    default = "us-east-2"
}

variable "instance_type" {
    description = "O tipo de instância EC2 a ser usada"
    type = string
    default = "t2.micro"
}

variable "vpc_ids" {
    description = "IDs das VPCs onde instancias EC2 serão criadas"
    type list(string)
}

variable "subnets" {
    description = "Subnets para instancias EC2 em cada VPC"
    type = list(string)
}

variable "ami_id" {
    description = "AMI ID pra instância"
    type = string
}