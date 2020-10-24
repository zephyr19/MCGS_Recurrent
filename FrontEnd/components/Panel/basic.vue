<template>
  <div class="basic">
    <div class="title">{{ title }}</div>
    <slot />
  </div>
</template>

<script>
export default {
  name: 'basic',
  props: {
    title: {
      required: true,
      type: String,
    },
  },
}
</script>

<style lang="scss">
.basic {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.title {
  color: #999;
  font-weight: bold;
  margin-right: 10px;
  overflow: hidden;
}
</style>
