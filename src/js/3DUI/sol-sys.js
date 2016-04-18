(function(global){

    "use strict";

    /**
     * Entry point for the 3D portion of the UI
     */

    global.SolSys = function(){

        this.debug = true;

        //Web GL, Three JS components
        this.camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
        this.scene = new THREE.Scene();
        this.renderer = new THREE.WebGLRenderer({antialias: true});
        this.viewPort = document.createElement("div");

        //Navigation
        this.currentMousePos = [0, 0];
        this.initialMousePos = [0, 0];
        this.cameraYaw = 45;//degrees
        this.cameraPitch = 45;//degrees
        this.yawRange = 540;//degrees
        this.pitchRange = 180;//degrees
        this.cameraDistance = 800;
        this.navigate = false;

        /**
         * start up function
         */
        this.initialize = function(){

            this.viewPort.id = "renderer-viewport";

            //mouse navigation events
            this.setupNavigationEventing();

            //set some up some reference markers
            this.drawEclipticPlane();

            //set up the render/camera/view
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.renderer.setClearColor(0x221d23, 1);

            //set initial camera position
            this.camera.position.x = Math.cos(this.cameraYaw * (Math.PI/180)) * this.cameraDistance;
            this.camera.position.y = Math.sin(this.cameraPitch * (Math.PI/180)) * this.cameraDistance;
            this.camera.position.z = Math.sin(this.cameraYaw * (Math.PI/180)) * this.cameraDistance;

            //add the view port to the DOM and start the render
            this.scene.add(new THREE.AmbientLight(0xffffff));

            this.viewPort.appendChild(this.renderer.domElement);
            document.body.appendChild(this.viewPort);

            //start the animation loop
            this.animate();
        };

        /**
         * Setup some axes for our reference
         */
        this.drawEclipticPlane = function(){

            var sunMaterial = new THREE.MeshBasicMaterial({color:0xf7d06b, wireframe:false, transparent:true, overdraw:true});
            var sun = new THREE.Mesh(new THREE.SphereGeometry(1), sunMaterial);
            sun.overdraw = true;
            this.scene.add(sun);
            
            //aligned with the X axis of the solar system, along the vernal equinox
            var xAxisMat = new THREE.LineBasicMaterial({color:0xd1636e, transparent:true, opacity:0.5});
            var xAxis = new THREE.Geometry();
            xAxis.vertices.push(new THREE.Vector3(2000, 0, 0));
            xAxis.vertices.push(new THREE.Vector3(-2000, 0, 0));
            var xAx = new THREE.Line(xAxis, xAxisMat);
            this.scene.add(xAx);

            var yAxisMat = new THREE.LineBasicMaterial({color:0x7c3a41, transparent:true, opacity:0.5});
            var yAxis = new THREE.Geometry();
            yAxis.vertices.push(new THREE.Vector3(0, 0, 2000));
            yAxis.vertices.push(new THREE.Vector3(0, 0, -2000));
            var yAxis = new THREE.Line(yAxis, yAxisMat);
            this.scene.add(yAxis);

            //used for calibration
            if(this.debug){

                /** 
                 * Three.js coord to Earth Centered Inertial
                 * RED   +X == -Y
                 * GREEN +Y == +Z
                 * BLUE  +Z == -X
                 */

                var axis = new THREE.AxisHelper(50);//red is X, green is Y, blue is Z
                axis.position.set(0, 0, 0);
                this.scene.add(axis);

                var loadUnitCircle = function(texture){

                    var unitCircleMat = new THREE.MeshBasicMaterial({transparent:true, opacity:0.6, side:THREE.DoubleSide, map:texture})
                    unitCircleMat.wrapS = unitCircleMat.wrapT = THREE.RepeatWrapping;
                    unitCircleMat.anisotropy = 16;
                    
                    //set to the Earth Centered Inertial Frame
                    var unitCircleGeom = new THREE.CircleGeometry(300, 32, 0, 2*Math.PI);
                    var unitCircle = new THREE.Mesh(unitCircleGeom, unitCircleMat);
                    unitCircle.rotation.x = -(Math.PI/2);
                    unitCircle.rotation.z = (Math.PI/2);

                    this.scene.add(unitCircle);
                }

                var unitCircleLoader = new THREE.TextureLoader();
                unitCircleLoader.load(

                    "/mpc/src/img/unit_circle.png",
                    loadUnitCircle.bind(this)
                );
            }
        };

        /**
         * Sets the eventing for the mouse movements 
         * so we can rotate the 3D graphics
         */
        this.setupNavigationEventing = function(){

            var setInitialMousePosition = function(event){

                this.initialMousePos[0] = event.pageX;
                this.initialMousePos[1] = event.pageY;
                this.navigate = true;
            };

            var setMousePositionDelta = function(event){

                if(!this.navigate) return;
                this.currentMousePos[0] = event.pageX - this.initialMousePos[0];
                this.currentMousePos[1] = event.pageY - this.initialMousePos[1];
            };

            var navigationEnd = function(event){

                this.cameraYaw = this.cameraYaw + ((this.yawRange/window.innerWidth)*this.currentMousePos[0]);
                this.cameraPitch = this.cameraPitch + ((this.pitchRange/(window.innerHeight))*this.currentMousePos[1]);

                this.currentMousePos[0] = 0;
                this.currentMousePos[1] = 0;
                this.navigate = false;
            };

            this.viewPort.addEventListener("mousedown",

                setInitialMousePosition.bind(this),
                false
            );

            this.viewPort.addEventListener("mousemove",

                setMousePositionDelta.bind(this),
                false
            );

            this.viewPort.addEventListener("mouseup", 
                
                navigationEnd.bind(this),
                false
            );

            this.viewPort.addEventListener("mouseout", 

                navigationEnd.bind(this),
                false
            );
        };

        /**
         * Refreshes the view and sets the camera position.
         */
        this.render = function(){

            if(this.navigate){
                
                /* 
                the current camera rotation plus 
                total degress of rotation divided by view port width times
                current total change in mouse position
                */
                var yaw = this.cameraYaw + ((this.yawRange/window.innerWidth) * this.currentMousePos[0]);
                this.camera.position.x = Math.cos(yaw * (Math.PI/180)) * this.cameraDistance;
                this.camera.position.z = Math.sin(yaw * (Math.PI/180)) * this.cameraDistance;

                var pitch = this.cameraPitch + ((this.pitchRange/(window.innerHeight)) * this.currentMousePos[1]);
                if(pitch > 90) this.cameraPitch = pitch = 90;
                if(pitch < -90) this.cameraPitch = pitch = -90;
                this.camera.position.y = Math.sin(pitch * (Math.PI/180)) * this.cameraDistance;
            }
            
            this.camera.lookAt(this.scene.position);
            this.renderer.render(this.scene, this.camera);
        }

        this.animate = function(){

            this.render();
            window.requestAnimationFrame(this.animate.bind(this));
        },

        //start up
        this.initialize();
    };
})(this);