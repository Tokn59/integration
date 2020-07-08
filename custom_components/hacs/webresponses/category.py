from aiohttp import web

from custom_components.hacs.helpers.functions.logger import getLogger
from custom_components.hacs.helpers.functions.path_exsist import async_path_exsist
from custom_components.hacs.share import get_hacs
from custom_components.hacs.webresponses.frontend import logger


async def async_serve_category_file(requested_file):
    hacs = get_hacs()
    logger = getLogger("web.category")
    try:
        if requested_file.startswith("themes/"):
            servefile = f"{hacs.system.config_path}/{requested_file}"
        else:
            servefile = f"{hacs.system.config_path}/www/community/{requested_file}"

        # Serve .gz if it exist
        if async_path_exsist(f"{servefile}.gz"):
            servefile += ".gz"

        if async_path_exsist(servefile):
            logger.debug(f"Serving {requested_file} from {servefile}")
            response = web.FileResponse(servefile)
            response.headers["Cache-Control"] = "no-store, max-age=0"
            response.headers["Pragma"] = "no-store"
            return response
        else:
            logger.error(f"Tried to serve up '{servefile}' but it does not exist")

    except (Exception, BaseException) as error:
        logger.debug(f"there was an issue trying to serve {requested_file} - {error}")

    return web.Response(status=404)
