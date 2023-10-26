import logging
import pathlib
import re

issue_template_folder = "./issue_template"

def configure_template(template: str) -> str:
    dicton_regex = re.compile(r"<<<(?P<dicton_name>\w+)_LIST>>>")

    for match in dicton_regex.finditer():
        dicton_name = match.groupdict()["dicton_name"]
        dicton_filename = pathlib.Path(f"dicton_{dicton_name.lower().replace(' ', '_')}.md")

        if not dicton_filename.exists():
            logging.warning(f"Could not configure dicton list for {dicton_name}. "
                            f"File {str(dicton_filename)} does not exist")
            continue

        dicton_list = dicton_filename.read_text()

        re.sub(rf"<<<{dicton_name}_LIST>>>", dicton_list, template)

    return template


def configure_all_issue_templates(issue_template_folder: str | pathlib.Path) -> None:

    for template_file in pathlib.Path(issue_template_folder).glob("*.yml"):
        with open(template_file, "r") as f:
            template = f.read()

            logging.info(f"Configured template {template_file}")

        pathlib.Path(f"./ISSUE_TEMPLATE/{template_file.name}").write_text(template)


if __name__ == "__main__":
    configure_all_issue_templates(issue_template_folder)    
