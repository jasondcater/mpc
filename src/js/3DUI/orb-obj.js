(function(global){

    "use strict";

    /**
     * Represents an object that orbits in the Solar System
     */

    global.OrbObj = function(anchor, scalar){

        this.scalar = scalar;
        this.anchor = anchor;

        //draw orbit using osculating orbital elements
        this.drawLineOrbit = function(orbitalElements){

            function degToRad(deg){

                return deg/180*Math.PI;
            } 

            var scale = this.scalar;
            var eccen = orbitalElements[11];
            var majAx = orbitalElements[12] * 2;
            var minAx = majAx * Math.sqrt(1-Math.pow(eccen,2));

            var inclination = orbitalElements[10];
            var ascendingNode = orbitalElements[9];
            var perihelion = orbitalElements[2]
            var argOfPerihelion = orbitalElements[8];

            //render the ellipse of the orbit, calc the major and minor axes 
            var ellipse = new THREE.EllipseCurve(0, 0, minAx*scale, majAx*scale, 0, 2.0*Math.PI, false);
            var ellipsePath = new THREE.CurvePath();
            ellipsePath.add(ellipse);
            var ellipseGeometry = ellipsePath.createPointsGeometry(100);

            //draw the ellipse and tilt the orbital plane for the inclination to the ecliptic 
            var material = new THREE.LineBasicMaterial({color:this.color, opacity:.8, linewidth:2, transparent:true});
            var orbit = new THREE.Line(ellipseGeometry, material);
            orbit.rotation.x = degToRad(90 + inclination);

            //rotate the orbit so the acending node crosses the ecliptic at the right position
            var center = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({color: 0xffff00}));
            center.rotation.y = degToRad(ascendingNode);

            //offset the origin of the orbit for the argument of the perihelion
            var offsetRadius = majAx - perihelion;
            
            var argPeri = degToRad(argOfPerihelion)//in radians
            var xOffset = offsetRadius * Math.cos(argPeri);
            var yOffset = offsetRadius * Math.sin(argPeri);
            center.position.x = -(xOffset*scale);
            center.position.z = yOffset*scale;//z = y, is due to the coordinate system conversion

            center.add(orbit);
            this.anchor.add(center);
        };

        //draw orbit using cartesian state vector
        this.drawPointOrbit = function(orbitalElements){

        };
    };
})(this);