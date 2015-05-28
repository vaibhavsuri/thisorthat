__author__ = 'ananyapoddar'

import getDynamoDB as db
import db_table_key_names as keys
import json

# Global Cache #
tags_cache = []
tags_cached = False


def cache_tags():
    global tags_cache, tags_cached
    if not tags_cached:
       # Cache tags from DB
        tags_cached = True
        tags_results = db.tag_db.scan()
        for tag in tags_results:
            single_tag = {}
            single_tag["id"] = int(tag[keys.tag_id])
            single_tag["name"] = tag[keys.tag_name]
            tags_cache.append(single_tag)

    return tags_cache


def send_tags():
    return json.dumps(cache_tags())