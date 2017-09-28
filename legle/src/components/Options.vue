<template>
    <div class="options-container abs animated fadeIn">
        <div @click="toggleDrawer" class="options-button" :class="isOnBackground?'background-text':'non-background-text'">
            <span class="fa fa-bars"></span>
        </div>

        <div class="options-drawer animated fadeInRight"
            :class="(isOnBackground?'background-text':'non-background-text')
            + ' ' + (drawerOpen ? '': 'zoomOutRight')">
            <span @click="onDepth(i-1)" v-for="i in 4" class="opt" :class="depth==i-1?'selected':''">{{i-1}} </span>
            <span class="fa fa-sort-amount-asc opt-icon"></span>
        </div>
    </div>
</template>

<script>
export default {
    props: [
        'isOnBackground'
    ],
    data() {
        return {
            drawerOpen: true,
            depth: 1,
        }
    },
    methods: {
        onDepth(depth) {
            this.depth = depth;
        },
        toggleDrawer() {
            this.drawerOpen = !this.drawerOpen;
        }
    }
}
</script>

<style>
.options-container {
    position: relative;
}

.options-button {
    position: absolute;
    transition: all cubic-bezier(0.215, 0.610, 0.355, 1) 200ms;
    right: 44px;
    top: 25px;
    font-size: 2.4em;
    cursor: pointer;
    padding: 0px 2px;
    z-index: 5;
    text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.24);
    opacity: 0.5;
}

.options-button:hover {
    opacity: 0.725;
    transform: scale(1.08);
}

.background-text {
    color: #fff;
}

.background-text:hover {
    color: #fff;
}

.non-background-text {
    color: #fff;
    opacity: 1;
}

.non-background-text:hover {
    opacity: 1;
    color: #fafafa;
}

.options-drawer {
    font-size: 1.1em;
    right: 45px;
    top: 74px;
    position: absolute;
}

.options-drawer span {
    font-size: 1.18em;
}

.opt-icon {
    opacity: 0.75;
}

.opt {
    cursor: pointer;
    opacity: 0.75;
    transition: all ease-in-out 125ms;
}

.opt:hover {
    font-size: 1.4em;
}

.opt.selected {
    font-size: 1.4em;
    font-weight: bold;
    opacity: 1;
}

</style>