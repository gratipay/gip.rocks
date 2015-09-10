import os
from aspen.website import Website

project_root = os.path.dirname(__file__)
www_root = os.path.join(project_root, 'www')
website = Website(project_root=project_root, www_root=www_root)


# Install the eval renderer.
# ==========================

from aspen import renderers

class Renderer(renderers.Renderer):
    def render_content(self, context):
        return eval(self.compiled, globals(), context)

class Factory(renderers.Factory):
    Renderer = Renderer

website.renderer_factories['eval'] = Factory(website)
