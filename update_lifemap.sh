#!/bin/sh

set -e

BUILD_DIRECTORY=build
SOLR_CONTAINER=lifemap-solr

# Update tree
echo "- BUILD TREE"
#rye run python tree/Main.py --skip-traversal --skip-add-info --skip-merge-jsons

# Update Solr
echo "- UPDATING SOLR"
echo "-- deleting taxo collection content"
docker exec -t $SOLR_CONTAINER /opt/solr/bin/solr post -c taxo -mode args -type application/xml '<delete><query>*:*</query></delete>'
docker exec -t $SOLR_CONTAINER /opt/solr/bin/solr post -c addi -mode args -type application/xml '<delete><query>*:*</query></delete>'
echo "-- Uploading tree features"
for num in $(seq 1 3); do
    docker cp $BUILD_DIRECTORY/TreeFeatures${num}.json $SOLR_CONTAINER:/opt/
    docker exec -t $SOLR_CONTAINER /opt/solr/bin/solr post -c taxo /opt/TreeFeatures${num}.json
    echo "== TreeFeatures${num} uploaded =="
done
echo "-- Uploading additional informations"
for num in $(seq 1 3); do
    docker cp $BUILD_DIRECTORY/ADDITIONAL.${num}.json $SOLR_CONTAINER:/opt/
    docker exec -t $SOLR_CONTAINER /opt/solr/bin/solr post -c addi /opt/ADDITIONAL.${num}.json
    echo "== ADDITIONAL.${num} uploaded =="
done

# Kill render_list-
echo "- KILL RENDER LIST"
#sudo killall render_list

# Remove ALL old tiles
echo "- REMOVE OLD TILES"
#sudo rm -r /var/lib/mod_tile/*

# Restart services
echo "- RESTART SERVICES"
#sudo service apache2 restart
#sudo service renderd restart
#sudo service renderdlist start

# Compute tiles for the 5 first zoom levels on 7 threads
echo "- PRERENDER TILES"
#/opt/mod_tile/render_list -n 7 < /usr/local/lifemap/XYZcoordinates >> /usr/local/lifemap/tilerenderer.log
#/opt/mod_tile/render_list -m onlylabels -n 7 < /usr/local/lifemap/XYZcoordinates >> /usr/local/lifemap/tilerenderer.log
#/opt/mod_tile/render_list -m nolabels -n 7 < /usr/local/lifemap/XYZcoordinates >> /usr/local/lifemap/tilerenderer.log
