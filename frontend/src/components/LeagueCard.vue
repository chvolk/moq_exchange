<template>
  <v-card>
    <v-card-title>{{ league.name }}</v-card-title>
    <v-card-text>
      <div>Type: {{ formatLeagueType(league.league_type) }}</div>
      <div>Members: {{ league.members.length }}/{{ league.max_members }}</div>
      <div>Trades per day: {{ league.trades_per_day }}</div>
      <div>
        Duration: {{ formatDate(league.start_date) }} - {{ formatDate(league.end_date) }}
      </div>
    </v-card-text>
    <v-card-actions>
      <v-btn
        color="primary"
        @click="$emit('view')"
      >
        View League
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  league: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['view'])

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

const formatLeagueType = (type) => {
  const types = {
    'STANDARD': 'Standard League',
    'RANDOM': 'Random Stocks',
    'PACK': 'Pack Draft',
    'CHAOS': 'Chaos League'
  }
  return types[type] || type
}
</script>
