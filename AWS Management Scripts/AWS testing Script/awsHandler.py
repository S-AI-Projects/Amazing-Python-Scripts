def _exact_instance_count_parameters(ami_id, count):
    return {
        "ImageId": ami_id,
        "MinCount": count,
        "MaxCount": count,
    }


def create_ec2(client, ami_id, count):
    client.run_instances(**_exact_instance_count_parameters(ami_id, count))


def create_ec2_snapshots(client, volume_id):
    client.create_snapshot(VolumeId=volume_id)


def create_ec2_volume(client, AZ):
    ab = client.create_volume(AZ)
    return ab


def create_vpc(client, cidr_block):
    client.create_vpc(CidrBlock=cidr_block)
