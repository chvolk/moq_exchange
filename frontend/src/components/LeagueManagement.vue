<template>
  <v-container>
    <h2>Leagues</h2>
    <v-tabs v-model="activeTab">
      <v-tab>My Leagues</v-tab>
      <v-tab>Leaderboard</v-tab>
    </v-tabs>

    <v-tabs-items v-model="activeTab">
      <v-tab-item>
        <v-btn @click="showCreateLeagueDialog = true">Create League</v-btn>
        <v-data-table
          :headers="headers"
          :items="leagues"
          class="elevation-1"
        >
          <template v-slot:item.actions="{ item }">
            <v-btn small @click="joinLeague(item)" v-if="!item.is_member">Join</v-btn>
            <v-btn small @click="leaveLeague(item)" v-else>Leave</v-btn>
          </template>
        </v-data-table>
      </v-tab-item>

      <v-tab-item>
        <v-select v-model="selectedLeague" :items="leagues" item-text="name" item-value="id" label="Select League"></v-select>
        <v-data-table
          :headers="leaderboardHeaders"
          :items="leaderboard"
          class="elevation-1"
        ></v-data-table>
      </v-tab-item>
    </v-tabs-items>

    <v-dialog v-model="showCreateLeagueDialog" max-width="500px">
      <v-card>
        <v-card-title>Create League</v-card-title>
        <v-card-text>
          <v-form @submit.prevent="createLeague">
            <v-text-field v-model="newLeague.name" label="League Name"></v-text-field>
            <v-text-field v-model="newLeague.max_members" label="Max Members" type="number"></v-text-field>
            <v-date-picker v-model="newLeague.start_date" label="Start Date"></v-date-picker>
            <v-date-picker v-model="newLeague.end_date" label="End Date"></v-date-picker>
            <v-btn type="submit">Create</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LeagueManagement',
  data: () => ({
    activeTab: 0,
    headers: [
      { text: 'Name', value: 'name' },
      { text: 'Members', value: 'members.length' },
      { text: 'Max Members', value: 'max_members' },
      { text: 'Start Date', value: 'start_date' },
      { text: 'End Date', value: 'end_date' },
      { text: 'Actions', value: 'actions', sortable: false },
    ],
    leaderboardHeaders: [
      { text: 'Rank', value: 'rank' },
      { text: 'User', value: 'user' },
      { text: 'Portfolio Value', value: 'portfolio_value' },
    ],
    leagues: [],
    leaderboard: [],
    selectedLeague: null,
    showCreateLeagueDialog: false,
    newLeague: {
      name: '',
      max_members: 10,
      start_date: null,
      end_date: null,
    },
  }),
  mounted() {
    this.fetchLeagues()
  },
  watch: {
    selectedLeague() {
      if (this.selectedLeague) {
        this.fetchLeaderboard()
      }
    }
  },
  methods: {
    async fetchLeagues() {
      try {
        const response = await axios.get('/api/leagues/')
        this.leagues = response.data
      } catch (error) {
        console.error('Error fetching leagues:', error)
      }
    },
    async createLeague() {
      try {
        await axios.post('/api/leagues/', this.newLeague)
        this.showCreateLeagueDialog = false
        this.fetchLeagues()
      } catch (error) {
        console.error('Error creating league:', error)
      }
    },
    async joinLeague(league) {
      try {
        await axios.post(`/api/leagues/${league.id}/join/`)
        this.fetchLeagues()
      } catch (error) {
        console.error('Error joining league:', error)
      }
    },
    async leaveLeague(league) {
      try {
        await axios.post(`/api/leagues/${league.id}/leave/`)
        this.fetchLeagues()
      } catch (error) {
        console.error('Error leaving league:', error)
      }
    },
    async fetchLeaderboard() {
      try {
        const response = await axios.get(`/api/leagues/${this.selectedLeague}/leaderboard/`)
        this.leaderboard = response.data.map((entry, index) => ({
          ...entry,
          rank: index + 1,
          portfolio_value: `$${entry.portfolio_value.toFixed(2)}`
        }))
      } catch (error) {
        console.error('Error fetching leaderboard:', error)
      }
    },
  },
}
</script>
