document.addEventListener("DOMContentLoaded", function() {
    const container = document.getElementById("threejs-container");
    if (!container) {
        console.error("Three.js container not found");
        return;
    }

    // Scene
    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / container.offsetHeight, 0.1, 1000);
    camera.position.z = 5;

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.offsetWidth, container.offsetHeight);
    renderer.setClearColor(0x222222); // Match CSS background
    container.appendChild(renderer.domElement);

    // Simple Cube Geometry
    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshStandardMaterial({ color: 0x007bff }); // Blue color
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 0.8);
    pointLight.position.set(2, 3, 4);
    scene.add(pointLight);

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

        cube.rotation.x += 0.005;
        cube.rotation.y += 0.005;

        renderer.render(scene, camera);
    }

    animate();

    // Handle window resize
    window.addEventListener("resize", () => {
        if (container.offsetWidth > 0 && container.offsetHeight > 0) {
            camera.aspect = container.offsetWidth / container.offsetHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.offsetWidth, container.offsetHeight);
        }
    });
});

