#!/usr/bin/env python
from util import rospy_compat
from opencaret_msgs.msg import RadarTracks, Obstacle
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from std_msgs.msg import ColorRGBA
from radar import RADAR_VALID_MAX

class RadarViz(rospy_compat.Node):
    def __init__(self):
        if not(rospy_compat.use_ros_1):
            super().__init__('radar_viz')
        rospy_compat.init_node(self, 'radar_viz')
        self.radar_sub = rospy_compat.Subscriber('/radar_tracks', RadarTracks, self.on_radar_tracks)
        self.radar_rviz_pub = rospy_compat.Publisher('/radar_viz', Marker, queue_size=1)
        self.lo_pub = rospy_compat.Subscriber('/lead_obstacle', Obstacle, self.on_lead_obstacle)

    def on_lead_obstacle(self, msg):
        marker = Marker()
        marker.header.frame_id = "middle_radar_link"
        if rospy_compat.use_ros_1:
            marker.header.stamp = rospy_compat.rospy.Time.now()
        marker.ns = "lead_obstacle"
        marker.id = 1
        marker.type = Marker.POINTS
        marker.action = Marker.MODIFY
        marker.scale.x = 0.5
        marker.scale.y = 0.5
        marker.scale.z = 0.1
        marker.color.r = 1.0
        marker.color.a = 1.0
        msg.point.y *= -1
        marker.points = [msg.point]
        marker.colors = [ColorRGBA(0.,0.,1.0,1.0)]
        self.radar_rviz_pub.publish(marker)

    def on_radar_tracks(self, msg):
        marker = Marker()
        marker.header.frame_id = "middle_radar_link"
        if rospy_compat.use_ros_1:
            marker.header.stamp = rospy_compat.rospy.Time(secs=msg.stamp.sec, nsecs=msg.stamp.nanosec)
        marker.ns = "radar_tracks"
        marker.id = 1
        marker.type = Marker.POINTS
        marker.action = Marker.MODIFY
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.1
        marker.color.r = 1.0
        marker.color.a = 1.0
        marker.points = []
        for track in msg.radar_tracks:
            p = Point()
            p.x = float(track.lng_dist)
            p.y = -float(track.lat_dist)
            p.z = 0.0
            c = ColorRGBA()
            c.a = float(track.valid_count) / RADAR_VALID_MAX
            if track.valid == True:
                c.r = 1.0
            else:
                c.a = 1.0
                c.r = c.g = c.b = 0.5

            marker.points.append(p)
            marker.colors.append(c)
        self.radar_rviz_pub.publish(marker)

    def get_marker_pc_for_track(self, lat_dist, lng_dist, valid_count):
        p = Point()
        p.x = float(lng_dist)
        p.y = -float(lat_dist)
        p.z = 0.0
        c = ColorRGBA()
        c.a = float(valid_count) / RADAR_VALID_MAX
        if valid_count > 0:
            c.r = 1.0
        else:
            c.a = 1.0
            c.r = c.g = c.b = 0.5
        return p, c

def main():
    rospy_compat.launch_node(RadarViz)

if __name__ == '__main__':
    main()
