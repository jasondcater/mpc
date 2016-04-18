(function(global){

    "use strict";

    /**
     * Represents an object that orbits in the Solar System
     */

    global.OrbObj = function(){

        this.name = "planet";
        this.color =  0x00ff00;
        this.aphelion = 1;//in AU
        this.perihelion = 1;//in AU
        this.majorAxis = 1;//in AU
        this.eccentricity = 0;
        this.inclination = 0;//to ecliptic
        this.ascendingNode = 0;
        this.anchor = null;
        this.argOfPerihelion = 0;
        this.planetSprite = null;
        this.scalar = 80;

        /**
         * start up function
         */
        this.initialize = function(orbit){

            //None
        };

        this.drawOrbit = function(){

            function degToRad(deg){

                return deg/180*Math.PI;
            } 

            //(Center_Xpos, Center_Ypos, Xradius, Yradius, StartAngle, EndAngle, isClockwise)
            var scale = this.scalar;
            var eccen = this.eccentricity;
            var majAx = this.majorAxis;
            var minAx = majAx * Math.sqrt(1-Math.pow(eccen,2));

            //render the ellipse of the orbit, calc the major and minor axes 
            var ellipse = new THREE.EllipseCurve(0, 0, minAx*scale, majAx*scale, 0, 2.0*Math.PI, false);
            var ellipsePath = new THREE.CurvePath();
            ellipsePath.add(ellipse);
            var ellipseGeometry = ellipsePath.createPointsGeometry(100);

            //draw the ellipse and tilt the orbital plane for the inclination to the ecliptic 
            var material = new THREE.LineBasicMaterial({color:this.color, opacity:.8, linewidth:2, transparent:true});
            var orbit = new THREE.Line(ellipseGeometry, material);
            orbit.rotation.x = degToRad(90 + this.inclination);

            //rotate the orbit so the acending node crosses the ecliptic at the right position
            var center = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({color: 0xffff00}));
            center.rotation.y = degToRad(this.ascendingNode);

            //offset the origin of the orbit for the argument of the perihelion
            var offsetRadius = majAx - this.perihelion;
            
            var argPeri = this.argOfPerihelion;
            var argPeri = degToRad(argPeri)//in radians
            var xOffset = offsetRadius * Math.cos(argPeri);
            var yOffset = offsetRadius * Math.sin(argPeri);
            center.position.x = -(xOffset*scale);
            center.position.z = yOffset*scale;//z = y, is due to the coordinate system conversion

            center.add(orbit);
            this.anchor.add(center);
        };

        //start up
        this.initialize();
    };
})(this);