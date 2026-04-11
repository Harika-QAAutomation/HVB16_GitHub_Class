import boto3
from botocore.exceptions import ClientError

DRY_RUN = True   # Set to False ONLY when you are 100% sure

def get_all_regions():
    ec2 = boto3.client("ec2")
    regions = ec2.describe_regions(AllRegions=True)
    return [r["RegionName"] for r in regions["Regions"] if r["OptInStatus"] != "not-opted-in"]

def confirm(msg):
    choice = input(f"{msg} (yes/no): ").strip().lower()
    return choice == "yes"

# ---------------- EC2 ---------------- #
def cleanup_ec2(region):
    ec2 = boto3.resource("ec2", region_name=region)
    instances = list(ec2.instances.filter(
        Filters=[{"Name": "instance-state-name", "Values": ["running", "stopped"]}]
    ))

    if not instances:
        return

    print(f"\n[EC2] Region {region}: {len(instances)} instance(s)")
    for inst in instances:
        print(f"  - {inst.id} ({inst.state['Name']})")

    if DRY_RUN:
        print("  DRY-RUN: No EC2 instances deleted")
        return

    if confirm(f"Delete ALL EC2 instances in {region}?"):
        for inst in instances:
            print(f"Deleting EC2 {inst.id}")
            inst.terminate()

# ---------------- ECS ---------------- #
def cleanup_ecs(region):
    ecs = boto3.client("ecs", region_name=region)
    clusters = ecs.list_clusters()["clusterArns"]

    for cluster in clusters:
        services = ecs.list_services(cluster=cluster)["serviceArns"]
        if not services:
            continue

        print(f"\n[ECS] Region {region}, Cluster {cluster}")
        for svc in services:
            print(f"  - Service: {svc}")

        if DRY_RUN:
            print("  DRY-RUN: No ECS services deleted")
            continue

        if confirm(f"Delete ECS services in cluster {cluster}?"):
            for svc in services:
                ecs.delete_service(
                    cluster=cluster,
                    service=svc,
                    force=True
                )
                print(f"Deleted ECS service {svc}")

# ---------------- RDS ---------------- #
def cleanup_rds(region):
    rds = boto3.client("rds", region_name=region)
    dbs = rds.describe_db_instances()["DBInstances"]

    if not dbs:
        return

    print(f"\n[RDS] Region {region}")
    for db in dbs:
        print(f"  - {db['DBInstanceIdentifier']}")

    if DRY_RUN:
        print("  DRY-RUN: No RDS deleted")
        return

    if confirm(f"Delete ALL RDS instances in {region}?"):
        for db in dbs:
            rds.delete_db_instance(
                DBInstanceIdentifier=db["DBInstanceIdentifier"],
                SkipFinalSnapshot=True,
                DeleteAutomatedBackups=True
            )
            print(f"Deleted RDS {db['DBInstanceIdentifier']}")

# ---------------- Lambda ---------------- #
def cleanup_lambda(region):
    lam = boto3.client("lambda", region_name=region)
    funcs = lam.list_functions()["Functions"]

    if not funcs:
        return

    print(f"\n[LAMBDA] Region {region}")
    for f in funcs:
        print(f"  - {f['FunctionName']}")

    if DRY_RUN:
        print("  DRY-RUN: No Lambda deleted")
        return

    if confirm(f"Delete ALL Lambda functions in {region}?"):
        for f in funcs:
            lam.delete_function(FunctionName=f["FunctionName"])
            print(f"Deleted Lambda {f['FunctionName']}")

# ---------------- MAIN ---------------- #
def main():
    regions = get_all_regions()
    print(f"Scanning {len(regions)} regions...")

    for region in regions:
        print(f"\n========== REGION: {region} ==========")
        cleanup_ec2(region)
        cleanup_ecs(region)
        cleanup_rds(region)
        cleanup_lambda(region)

    print("\n✅ Cleanup completed")

if __name__ == "__main__":
    main()
