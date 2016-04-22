(function(global){

    "use strict";

    /**
     * Represents an object that orbits in the Solar System
     *
     * A good table of element calculation can be found here:
     * http://www.bogan.ca/orbits/kepler/orbteqtn.html
     */

    global.OrbObj = function(anchor, scalar){

        this.scalar = scalar;
        this.anchor = anchor;
        this.color  = 0x6666cc;

        //draw orbit using osculating orbital elements
        this.drawLineOrbit = function(orbitalElements){

            var scale = this.scalar;
            var eccentricity = orbitalElements[11];
            var semiMajAx = orbitalElements[12];
            var semiMinAx = semiMajAx * Math.sqrt(1-Math.pow(eccentricity,2));

            var argOfPerihelion = orbitalElements[8];
            var ascendingNode = orbitalElements[9];
            var inclination = orbitalElements[10];

            //calculate the perihelion; q = a (1 - e)
            var perihelion = semiMajAx * (1 - eccentricity);

            //render the ellipse of the orbit, calc the major and minor axes 
            var ellipse = new THREE.EllipseCurve(0, 0, semiMinAx*scale, semiMajAx*scale, 0, 2*Math.PI, false);
            var ellipsePath = new THREE.CurvePath();
            ellipsePath.add(ellipse);
            var ellipseGeometry = ellipsePath.createPointsGeometry(100);

            //draw the ellipse
            var material = new THREE.LineBasicMaterial({color:this.color, opacity:.8, linewidth:2, transparent:true});
            var orbit = new THREE.Line(ellipseGeometry, material);

            //perihelion offset
            var offset = (semiMajAx - perihelion) * scale;
            orbit.position.y = -(offset);

            //tilt the ellipse for the inclination
            orbit.rotation.x = this.degToRad(inclination);

            //rotate the orbit so the acending node crosses the ecliptic at the right position
            var center = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({color: 0xffff00}));
            center.rotation.x = -(Math.PI/2);
            center.rotation.z = this.degToRad(ascendingNode);

            center.add(orbit);
            this.anchor.add(center);
        };

        //draw orbit using cartesian state vector
        this.drawPointOrbit = function(orbitalElements){

            // create the particle variables
            var particleCount = orbitalElements.length;
            var particles = new THREE.Geometry();
            var particleMat = new THREE.PointsMaterial({

                color: 0xcc9966,
                size: 1.0
            });

            for(var a = 0; a < particleCount; ++a){

                var pX = orbitalElements[a][1] * this.scalar;
                var pY = orbitalElements[a][2] * this.scalar;
                var pZ = orbitalElements[a][3] * this.scalar;
                var particle = new THREE.Vector3(pX, pY, pZ);
                particles.vertices.push(particle);
            }
            
            var particleSystem = new THREE.Points(particles, particleMat);

            var center = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({color: 0xffff00}));
            center.rotation.x = -(Math.PI/2)
            center.add(particleSystem);
            this.anchor.add(center);
        };

        this.degToRad = function(deg){

            return deg/180*Math.PI;
        };
    };
})(this);