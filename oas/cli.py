import argparse

"""
We sort of have to re-make the CLI project because OAS is just too big now. I am gonna make it so it acts more like
this IDE where you can open a project file and work within a project rather than run one command. 

Now we can like add and edit things like calibration and havemultiple video files in one folder and it will be easier
for inter-trial stats - this will all be in ~/OAS-Engine/ProjectManager
"""







def main():
    parser = argparse.ArgumentParser(
        prog="Oromotor Asymmetry System (OAS) CLI",
        description="OAS Calculates mouth movement and compares that to a praat analysis."
    )
    subparsers = parser.add_subparsers(dest="target")

    # PROJECT LEVEL COMMANDS/ARGUMANTS

    project_parser = subparsers.add_parser("project", help="Project level commands")
    project_sub = project_parser.add_subparsers(dest="action")

    project_create = project_sub.add_parser("create", help="Create a new OAS project")
    project_create.add_argument("path")
    project_create.add_argument("name")

    project_delete = project_sub.add_parser("delete", help="Delete an OAS project")
    project_delete.add_argument("path")

    args = parser.parse_args()

    if args.target == "project":
        if args.action == "create":

            print(f"project path: {args.path}\nProject Name{args.name}")
            from oas.ProjectManager.project_creation import ProjectCreation
            ProjectCreation().project_creation(args.path, args.name)

        elif args.action == "delete":
            print(f"Deleting ~/{args.path}\nWill add actual logic later")

    # PARTICIPANT LEVEL COMMANDS/ARGUMENTS

    participant_parser = ubparsers.add_parser("participant", help="Participant level commands")



    # TRIAL LEVEL COMMANDS/ARGUMENTS



"""

HOW TO USE CLI:

When running locally from command terminal, use:

> source .venv/bin/activate

Then use: 

> python -m oas.cli -m (mode) -f (input file) -o (output file) -f (force) -start (compute at row int) -end (finish at row int)

CLI testing command

python3 -m oas.cli -m init -f "data/test-data/v15044gf0000d1dlc67og65r2deqmhd0.csv" --force --pose

"""

if __name__ == "__main__":
    main()