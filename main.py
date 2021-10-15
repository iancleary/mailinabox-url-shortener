"""URL Shortener Hack"""
import json
import os
import shutil

EXISTING_MAIL_IN_A_BOX_ROUTES = {"admin", "cloud", "mail"}

def remove_mail_in_a_box_internal_links(links):
    # remove protected links
    ret = [x for x in links if x["name"] not in EXISTING_MAIL_IN_A_BOX_ROUTES]
    return ret

def remove_mail_in_a_box_folders_from_dist():
    # remove protected folders to ensure
    for folder in EXISTING_MAIL_IN_A_BOX_ROUTES:
        shutil.rmtree(f'dist/{folder}', ignore_errors=True)

def main():
    """Main Function"""
    html = '<html><head><meta http-equiv="refresh" content="0;url={url}" /></head></html>'

    with open('links.json') as f:
        links = json.load(f)

    shutil.rmtree('dist', ignore_errors=True)
    os.mkdir('dist')

    with open('dist/CNAME', 'w') as f:
        f.write('iancleary.me')


    links = remove_mail_in_a_box_internal_links(links)

    for link in links:
        html_document = html.format(url=link['url'])

        if link["name"] == "index":
            # index is www root
            file_path = "dist/index.html"
        else:
            # need to make folder for route
            os.mkdir(f"dist/{link['name']}")
            file_path = f"dist/{link['name']}/index.html"

        with open(file_path, 'w') as f:
            f.write(html_document)

    remove_mail_in_a_box_folders_from_dist()

if __name__ == "__main__":
    main()
