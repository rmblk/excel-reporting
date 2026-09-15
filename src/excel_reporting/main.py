import argparse

from dotenv import load_dotenv

from excel_reporting.sps import build


def run():
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--report", required=True, choices=["sps"])
    parser.add_argument(
        "-f", "--file", type=str, required=False, help="Path to the output Excel file."
    )
    parser.add_argument(
        "-e",
        "--env-file",
        type=str,
        required=False,
        help="Path to the .env file. If not provided, defaults to .env in the current directory.",
    )
    parser.add_argument(
        "-m",
        "--memory",
        action="store_true",
        help="Store the report in memory, do not write to disk.",
    )

    args, remaining = parser.parse_known_args()
    if args.env_file:
        load_dotenv(args.env_file)
    else:
        load_dotenv()

    match args.report:
        case "sps":
            data = build()
        case _:
            raise ValueError(f"Unknown report: {args.report}")

    if args.memory:
        # Do something with the generated data, e.g., upload it or process it
        pass
    else:
        # Write the generated data to a file
        if not args.file:
            raise ValueError(
                "Output file path must be specified when not using --memory."
            )
        with open(args.file, "wb") as f:
            f.write(data)


if __name__ == "__main__":
    run()
