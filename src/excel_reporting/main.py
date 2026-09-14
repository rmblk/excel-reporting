import argparse


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--report", required=True, choices=[])
    parser.add_argument(
        "-f", "--file", type=str, required=False, help="Path to the output Excel file."
    )
    parser.add_argument(
        "-m",
        "--memory",
        action="store_true",
        help="Store the report in memory, do not write to disk.",
    )

    args, remaining = parser.parse_known_args()

    match args.report:
        case "example":
            pass
        case _:
            raise ValueError(f"Unknown report: {args.report}")


if __name__ == "__main__":
    run()
