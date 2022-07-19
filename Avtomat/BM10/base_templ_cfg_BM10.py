import os
import yaml
from jinja2 import Environment, FileSystemLoader


def generate_config(template, data_dict):
    templ_dir, templ_file = os.path.split(template)
    env = Environment(loader=FileSystemLoader (templ_dir))
    templ = env.get_template(templ_file)
    return templ.render(data_dict)
if __name__ == "__main__":
    data_fle = "data_file/router_net.yaml"
    template_file = "templates/base_cfg.txt"
    with open(data_fle) as f:
        data = yaml.safe_load(f)
    print(generate_config(template_file, data))