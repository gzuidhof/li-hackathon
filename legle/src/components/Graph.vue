<template>
  <div class="graph-view">
      <div class="red-background fs abs" :class="showRedBackground ? '':'hide'"></div>
      <div class="center-greeting animated fadeIn" :class="showRedBackground ? '':'hide'">legle</div>
  </div>
</template>

<script>
export default {
  name: 'main',
  props: ['showRedBackground'],
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.graph-view {
    width: 100%;
    height: 100%;
    background-color: #f2f2f2;
    position: absolute;
    z-index: 0;
}

.red-background {
    background: linear-gradient(270deg, #c60808, #f75959);
    transition: all ease-in-out 500ms;
    position: absolute;
    z-index: 1;
    pointer-events: none;
}

.red-background.hide{
    opacity: 0;
}

.center-greeting {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    color: #fff;
    font-size: 12.5em;
    z-index: 2;
    text-shadow: 1px 2px 3px rgba(0, 0, 0, 0.3);
    transition: all ease-in-out 200ms;
    opacity: 1;
}

.center-greeting.hide{
    opacity: 0;
    visibility: hidden;
}
</style>
