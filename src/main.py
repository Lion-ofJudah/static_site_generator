import os
import shutil

from block import markdown_to_html_node, extract_title


def main():
    copy_content(source_directory="./static", destination_directory="./public")
    generate_pages_recursive(
        dir_path_content="./content",
        template_path="./template.html",
        dest_dir_path="./public",
    )
    # generate_page(
    #     from_path="./content/index.md",
    #     template_path="./template.html",
    #     dest_path="./public/index.html",
    # )
    # generate_page(
    #     from_path="./content/blog/glorfindel/index.md",
    #     template_path="./template.html",
    #     dest_path="./public/blog/glorfindel/index.html",
    # )
    # generate_page(
    #     from_path="./content/blog/majesty/index.md",
    #     template_path="./template.html",
    #     dest_path="./public/blog/majesty/index.html",
    # )
    # generate_page(
    #     from_path="./content/blog/tom/index.md",
    #     template_path="./template.html",
    #     dest_path="./public/blog/tom/index.html",
    # )
    # generate_page(
    #     from_path="./content/contact/index.md",
    #     template_path="./template.html",
    #     dest_path="./public/contact/index.html",
    # )


def copy_content(source_directory: str, destination_directory: str):
    if os.path.exists(destination_directory):
        shutil.rmtree(destination_directory)

    os.mkdir(destination_directory)
    files = os.listdir(source_directory)

    for file in files:
        if os.path.isfile(f"{source_directory}/{file}"):
            shutil.copy(f"{source_directory}/{file}", destination_directory)
        else:
            os.mkdir(f"{destination_directory}/{file}")
            copy_content(
                f"{source_directory}/{file}", f"{destination_directory}/{file}"
            )


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    os.makedirs(dest_dir_path, exist_ok=True)
    contents = os.listdir(dir_path_content)

    for content in contents:
        if os.path.isfile(f"{dir_path_content}/{content}"):
            html_filename = os.path.splitext(content)[0] + ".html"
            generate_page(
                from_path=f"{dir_path_content}/{content}",
                template_path=template_path,
                dest_path=f"{dest_dir_path}/{html_filename}",
            )
        else:
            os.makedirs(f"{dest_dir_path}/{content}")
            generate_pages_recursive(
                dir_path_content=f"{dir_path_content}/{content}",
                template_path=template_path,
                dest_dir_path=f"{dest_dir_path}/{content}",
            )
    pass


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as md_file:
        markdown = md_file.read()

    with open(template_path, "r") as html_file:
        template_html = html_file.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown=markdown).to_html()

    template_html = template_html.replace("{{ Title }}", title)
    template_html = template_html.replace("{{ Content }}", html)

    with open(dest_path, "w") as file:
        file.write(template_html)


if __name__ == "__main__":
    main()
