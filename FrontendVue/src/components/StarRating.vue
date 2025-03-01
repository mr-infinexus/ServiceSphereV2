<template>
    <span>
        <i v-for="n in fullStars" :key="n" class="bi bi-star-fill"></i>
        <i v-if="halfStar" class="bi bi-star-half"></i>
        <i v-if="rating == 0" class="bi bi-star"></i>
    </span>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
    rating: {
        type: Number,
        required: true
    }
});

const fullStars = ref(Math.floor(props.rating));
const halfStar = ref((props.rating - fullStars.value) >= 0.1);
</script>

<style scoped>
.bi {
    color: gold;
    text-shadow: 0px 0px 1px black;
}
</style>