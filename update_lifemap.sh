#!/bin/sh

# Update tree
echo "- BUILD TREE"
rye run python tree/Main.py --skip-traversal --skip-add-info --skip-merge-jsons

# Update Solr
# TODO

# Kill render_list
echo "- KILL RENDER LIST"
sudo killall render_list

# Remove ALL old tiles
echo "- REMOVE OLD TILES"
sudo rm -r /var/lib/mod_tile/*

# Restart services
echo "- RESTART SERVICES"
sudo service apache2 restart
sudo service renderd restart
sudo service renderdlist start

# Compute tiles for the 5 first zoom levels on 7 threads
echo "- PRERENDER TILES"
/opt/mod_tile/render_list -n 7 < /usr/local/lifemap/XYZcoordinates >> /usr/local/lifemap/tilerenderer.log
/opt/mod_tile/render_list -m onlylabels -n 7 < /usr/local/lifemap/XYZcoordinates >> /usr/local/lifemap/tilerenderer.log
/opt/mod_tile/render_list -m nolabels -n 7 < /usr/local/lifemap/XYZcoordinates >> /usr/local/lifemap/tilerenderer.log
