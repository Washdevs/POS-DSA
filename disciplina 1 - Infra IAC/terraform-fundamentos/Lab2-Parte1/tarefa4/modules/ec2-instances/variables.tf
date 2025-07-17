variable "instance_count" {
    description = "Quantidade de instância EC2 a ser usada"
    type = number
}

variable "ami_id" {
    description = "AMI ID pra instância"
    type = string
}

variable "instance_type" {
    description = "O tipo de instância EC2 a ser usada"
    type = string
    default = "t2.micro"
}

variable "subnet_id" {
    description = "Subnet id para instancias EC2"
    type = string
}