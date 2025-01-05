<template>
  <div :data-id="index" class="card-body">
    <div class="d-flex gap-2">
      <v-text-field v-model="requestData.name" :rules="[rules.required]" type="text" placeholder="Name" variant="solo-filled" flat />
      <v-combobox v-model="requestData.genre" :items="genres" :rules="[rules.required]" type="text" placeholder="Genre" variant="solo-filled" flat />
      <v-text-field v-model="requestData.year" :rules="[rules.year]" type=" text" placeholder="Year" variant="solo-filled" flat />
    </div>

    <v-text-field v-model="requestData.difficulty" :rules="[rules.difficulty]" :min="1" :max="5" type="number" placeholder="Difficulty" variant="solo-filled" flat />

    <div class="d-flex gap-2">
      <v-text-field v-model="requestData.artist" :rules="[rules.required]" type="text" placeholder="Artist" variant="solo-filled" flat />
      <v-text-field v-model="requestData.youtube" :rules="[rules.required]" type="url" placeholder="YouTube" variant="solo-filled" flat />
    </div>

    <v-text-field v-model="iframe" variant="solo-filled" placeholder="Iframe parser" flat @keypress.enter="handleParseIframe" />
  </div>
</template>

<script lang="ts" setup>
import type { CreateData } from '@/types';
import { computed, inject, PropType, reactive, ref } from 'vue';
import { useDayJs } from '@/plugins';

const { currentYear } = useDayJs()

const props = defineProps({
  block: {
    type: Object as PropType<CreateData>,
    default: () => ({
      name: '',
      genre: '',
      artist: '',
      youtube: '',
      year: null,
      difficulty: 1
    })
  },
  index: {
    type: Number,
    required: true
  }
})

const fieldErrors = reactive({
  name: '',
  genre: '',
  artist: '',
  youtube: '',
  year: ''
});

const iframe = ref<string>('')

const rules = {
  required: (v: string) => !!v || 'This field is required',
  youtubeUrl: (v: string) => {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$/;
    return youtubeRegex.test(v) || 'Please enter a valid YouTube URL';
  },
  difficulty: (v: number) => {
    return v <= 5 || 'Difficulty should be between 1 and 5'
  },
  year: (v: number | null) => {
    if (!v) {
      return true
    } else {
      return (v >= 1900 && v <= currentYear.value) || `Year must be between 1900 and ${currentYear.value}`;
    }
  }
}

// Validation function
function validateData(data: CreateData) {
  const errors: Record<string, string> = {};
  
  Object.keys(fieldErrors).forEach(key => {
    fieldErrors[key as keyof typeof fieldErrors] = '';
  });

  if (!data.name) {
    errors.name = 'Name is required'
  }
  
  if (!data.genre) {
    errors.genre = 'Genre is required'
  }

  if (!data.artist) {
    errors.artist = 'Artist is required'
  }
  
  // YouTube URL validation
  if (!data.youtube) {
    errors.youtube = 'YouTube URL is required';
  } else if (!rules.youtubeUrl(data.youtube)) {
    errors.youtube = 'Please enter a valid YouTube URL';
  }
  
  // Year validation (optional but must be valid if provided)
  if (data.year !== null && !rules.year(data.year)) {
    errors.year = `Year must be between 1900 and ${currentYear}`;
  }

  // Update field errors
  Object.entries(errors).forEach(([key, value]) => {
    fieldErrors[key as keyof typeof fieldErrors] = value;
  });

  return errors;
}

const emit = defineEmits({
  'update:block' (_data: CreateData) {
    return true
  }
})

const requestData = computed({
  get: () => props.block,
  set: (value) => {
    const errors = validateData(value)
    console.log(errors)
    emit('update:block', value)
  }
})

const genres = inject<string[]>('genres')

function handleParseIframe () {
  const regex = /src="([^"]*)"/;
  const match = iframe.value.match(regex);

  if (match) {
    requestData.value.youtube = match[1]
    iframe.value = ''
  }
}
</script>
