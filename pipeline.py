import argparse
import json
from collections import namedtuple

PreferenceMatch = namedtuple("PreferenceMatch", ["product_name", "product_codes"])


def main(product_data, include_tags, exclude_tags):
    """The implementation of the pipeline test."""

    preference_list = []

    for items in product_data:
        if any(tag in include_tags for tag in items["tags"]) and not any(tag in exclude_tags for tag in items["tags"]):
            preference_list.append(PreferenceMatch(items["name"], items["code"]))

    return preference_list




if __name__ == "__main__":

    def parse_tags(tags):
        return [tag for tag in tags.split(",") if tag]

    parser = argparse.ArgumentParser(
        description="Extracts unique product names matching given tags."
    )
    parser.add_argument(
        "product_data",
        help="a JSON file containing tagged product data",
    )
    parser.add_argument(
        "--include",
        type=parse_tags,
        help="a comma-separated list of tags whose products should be included",
        default="",
    )
    parser.add_argument(
        "--exclude",
        type=parse_tags,
        help="a comma-separated list of tags whose matching products should be excluded",
        default="",
    )

    args = parser.parse_args()

    with open(args.product_data) as f:
        product_data = json.load(f)

    order_items = main(product_data, args.include, args.exclude)

    for item in order_items:
        print("%s:\n%s\n" % (item.product_name, item.product_codes))
