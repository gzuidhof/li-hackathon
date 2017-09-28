<template>
    <div class="options-container abs animated fadeIn">
        <div class="options-button" :class="isOnBackground?'':'non-background-text'">
            <span class="fa fa-bars"></span>
        </div>
    </div>
</template>

<script>
export default {
    props: [
        'isOnBackground'
    ]
}
</script>

<style>
.options-container {
    position: relative;
}

.options-button {
    position: absolute;
    transition: all cubic-bezier(0.215, 0.610, 0.355, 1) 200ms;
    right: 40px;
    top: 22px;
    font-size: 2.4em;
    color: #fff;
    opacity: 0.5;
    cursor: pointer;
    padding: 0px 2px;
    z-index: 5;
    text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.24);
}

.options-button:hover {
    opacity: 0.725;
    transform: scale(1.08);
}

.non-background-text {
    color: #fff;
    opacity: 1;
}

.non-background-text:hover {
    opacity: 1;
    color: #fafafa;
}
</style>