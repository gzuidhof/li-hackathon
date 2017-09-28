<template>
    <div class="options-container abs fs animated fadeIn">
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
}

.options-button:hover {
    opacity: 0.725;
    transform: scale(1.08);
}

.non-background-text {
    color: #236fb1;
    opacity: 1;
}
</style>