const ourStory = document.getElementById("our-story");

window.addEventListener("scroll", function() {
    setTimeout(() => {
        ourStory.style.display = "flex";
        ourStory.style.opacity = 1;
        ourStory.style.animation = "fadeIn 2s";
    }, 450);
});

console.log("test")