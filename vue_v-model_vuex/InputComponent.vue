<template>
  <div>
    <!-- v-model bind to local computed property 'message' -->
    <input v-model="message" placeholder="type something...">
    {{ message }}
  </div>
</template>

<script>
export default {
  name: 'input-component',
  computed: {
    message: {
      // custome get() and set() of this local computed property
      get () {
        // get stored message
        return this.$store.state.message;
      },
      set (newMessage) {
        // commit a mutation to set message
        this.$store.commit('setMessage', newMessage);
      }
    }
  }
}
</script>

<style scoped>
</style>
