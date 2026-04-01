<template>
  <v-container>
    <h1 class="mb-4">Your Leagues</h1>
    <v-btn color="primary" class="mb-4">Create New League</v-btn>
    <v-list two-line>
      <v-list-item v-for="league in leagues" :key="league.id">
        <v-list-item-content>
          <v-list-item-title>{{ league.name }}</v-list-item-title>
          <v-list-item-subtitle>Members: {{ league.memberCount }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn text color="primary">View</v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
export default {
  name: 'LeaguesPage',
  data: () => ({
    leagues: [
      { id: 1, name: 'Tech Titans', memberCount: 8 },
      { id: 2, name: 'Wall Street Warriors', memberCount: 10 },
      // Add more mock data as needed
    ],
  }),
  // Add methods for fetching leagues, creating new leagues, etc.
}
</script>