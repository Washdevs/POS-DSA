provider "aws" {
    region = "us-east-2"
}

resource "aws_vpc" "redshift_vpc" { # "recurso" "nome do meu recurso"
  cidr_block = "10.0.0.0/16" # Range de endereços IPS para esta VPC
 
  tags = {
    Name = "DSA redshift_vpc" # Descrição
  }
}

resource "aws_subnet" "redshift_subnet"{
  cidr_block = "10.0.1.0/24"
  vpc_id = aws_vpc.redshift_vpc.id

  tags = {
    Name = "DSA Redshift Subnet"
  }
}

