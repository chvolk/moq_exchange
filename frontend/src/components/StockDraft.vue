<template>
  <v-container fluid class="fill-height pa-0" style="background: linear-gradient(to right, #4CAF50, #2196F3);">
    <v-row align="center" justify="center" class="mx-0">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="12" class="pa-6">
          <v-card-title class="draft-title text-h4 font-weight-bold text-center mb-4">
            Moq Draft
          </v-card-title>
          
          <v-card-subtitle class="text-h5 text-center mb-4">
            Available Balance: ${{ formattedBalance }}
          </v-card-subtitle>
          
          <v-row>
            <v-col cols="12" md="8">
              <v-card outlined>
                <v-card-title>Available Stocks</v-card-title>
                <v-card-text>
                  <v-row>
                    <v-col cols="12" sm="6">
                      <v-autocomplete
                        v-model="selectedIndustries"
                        :items="industries"
                        label="Filter by Industry"
                        multiple
                        chips
                        small-chips
                        deletable-chips
                        clearable
                        dense
                        outlined
                      ></v-autocomplete>
                    </v-col>
                    <v-col cols="12" sm="6">
                      <v-text-field
                        v-model.number="maxPriceFilter"
                        label="Max Price"
                        type="number"
                        clearable
                        outlined
                        dense
                        prefix="$"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-data-table
                    :headers="headers"
                    :items="filteredStocks"
                    :search="search"
                    :options.sync="tableOptions"
                    @update:options="updateTableOptions"
                    :items-per-page="tableOptions.itemsPerPage"
                    :page.sync="tableOptions.page"
                    :sort-by="tableOptions.sortBy"
                    :sort-desc="tableOptions.sortDesc"
                    class="elevation-1"
                    height="400px"
                    sortable
                  >
                    <template v-slot:top>
                      <v-text-field
                        v-model="search"
                        append-icon="mdi-magnify"
                        label="Search"
                        :sort-by="sortBy"
                        :sort-desc="sortDesc"
                        
                        single-line
                        hide-details
                        class="mb-4"
                      ></v-text-field>
                    </template>
                    <template v-slot:item.current_price="{ item }">
                      ${{ item.current_price }}
                    </template>
                    <template v-slot:item.industry="{ item }">
                      {{ item.industry || 'N/A' }}
                    </template>
                    <template v-slot:item.actions="{ item }">
                      <v-btn small color="primary" @click="openDraftDialog(item)">Draft</v-btn>
                    </template>
                  </v-data-table>
                </v-card-text>
              </v-card>
            </v-col>
            
            <v-col cols="12" md="4">
              <v-card outlined>
                <v-card-title>Your Portfolio</v-card-title>
                <v-card-text style="height: 400px; overflow-y: auto;">
                  <v-list dense>
                    <v-list-item v-for="stock in portfolio" :key="stock.stock.symbol">
                      <v-list-item-content>
                        <v-list-item-title>{{ stock.stock.symbol }}</v-list-item-title>
                        <v-list-item-subtitle>
                          {{ stock.quantity }} shares @ ${{ stock.stock.current_price }}
                        </v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-action>
                        ${{ (stock.quantity * stock.stock.current_price).toFixed(2) }}
                      </v-list-item-action>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Draft Dialog -->
    <v-dialog v-model="draftDialog" max-width="400px">
      <v-card>
        <v-card-title>Draft Shares</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <p>Stock: {{ selectedStock ? selectedStock.name : '' }}</p>
              <p>Current Price: ${{ selectedStock ? Number(selectedStock.current_price).toFixed(2) : '0.00' }}</p>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model.number="draftQuantity"
                label="Number of Shares"
                type="number"
                min="1"
                :rules="[v => v > 0 || 'Quantity must be greater than 0']"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <p class="font-weight-bold">Total Cost: ${{ totalCost.toFixed(2) }}</p>
              <p :class="{'error--text': totalCost > balance}">
                Remaining Balance: ${{ (balance - totalCost).toFixed(2) }}
              </p>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeDraftDialog">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="confirmDraft" :disabled="!canDraft">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" top>
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'StockDraft',
  data: () => ({
    headers: [
      { title: 'Symbol', value: 'symbol', sortable: true },
      { title: 'Name', value: 'name', sortable: true },
      { title: 'Industry', value: 'industry', sortable: true },
      { title: 'Current Price', value: 'current_price', sortable: true },
      { title: 'Actions', value: 'actions', sortable: false }
    ],
    availableStocks: [],
    draftedStocks: [],
    search: '',
    loading: false,
    error: null,
    selectedIndustries: [],
    maxPriceFilter: '',
    industries: [],
    sortBy: 'symbol', // Default sort column
    sortDesc: false, // Def
    snackbar: false,
    snackbarText: '',
    snackbarColor: 'success',
    draftDialog: false,
    selectedStock: null,
    draftQuantity: 1,
    balance: 0,
    portfolio: [],
    tableOptions: {
      sortBy: ['symbol'],
      sortDesc: [false],
      page: 1,
      itemsPerPage: 10
    },
  }),
  computed: {
    filteredStocks() {
    let stocks = this.availableStocks.filter(stock => {
      const matchesIndustry = this.selectedIndustries.length === 0 || 
        (stock.industry && this.selectedIndustries.includes(stock.industry));
      const matchesPrice = !this.maxPriceFilter || 
        (stock.current_price && stock.current_price <= parseFloat(this.maxPriceFilter));
      const isValidPrice = stock.current_price && stock.current_price >= 0.01; // New condition
      return matchesIndustry && matchesPrice && isValidPrice; // Include new condition
    });

    // Apply sorting
    if (this.tableOptions && this.tableOptions.sortBy && this.tableOptions.sortBy.length) {
      const sortBy = this.tableOptions.sortBy[0];
      const sortDesc = this.tableOptions.sortDesc ? this.tableOptions.sortDesc[0] : false;
      stocks = stocks.sort((a, b) => {
        let comparison = 0;
        if (a[sortBy] < b[sortBy]) comparison = -1;
        if (a[sortBy] > b[sortBy]) comparison = 1;
        return sortDesc ? -comparison : comparison;
      });
    }

    return stocks;
  },
    formattedBalance() {
      return typeof this.balance === 'number' ? this.balance.toFixed(2) : '0.00'
    },
    totalCost() {
      if (this.selectedStock && this.draftQuantity > 0) {
        return Number(this.selectedStock.current_price) * this.draftQuantity;
      }
      return 0;
    },
    canDraft() {
      return this.draftQuantity > 0 && this.totalCost <= this.balance;
    }
  },
  mounted() {
    this.fetchAvailableStocks();
    this.fetchPortfolio();
  },
  methods: {
    async fetchAvailableStocks() {
      this.loading = true;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/stocks/available/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        });
        this.availableStocks = response.data.map(stock => ({
          ...stock,
          current_price: Number(stock.current_price)
        }));
        this.industries = [...new Set(this.availableStocks
          .map(stock => stock.industry)
          .filter(industry => industry)
        )].sort();
      } catch (error) {
        console.error('Error fetching stocks:', error);
        this.error = 'Failed to fetch available stocks. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    async fetchPortfolio() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/portfolio/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        });
        this.portfolio = response.data.stocks;
        this.balance = Number(response.data.balance);
      } catch (error) {
        console.error('Error fetching portfolio:', error);
      }
    },
    openDraftDialog(stock) {
      this.selectedStock = {
        ...stock,
        current_price: Number(stock.current_price)
      };
      this.draftQuantity = 1;
      // Delay opening the dialog
      setTimeout(() => {
        this.draftDialog = true;
      }, 0);
    },
    closeDraftDialog() {
      this.draftDialog = false;
      this.selectedStock = null;
      this.draftQuantity = 1;
    },
    async confirmDraft() {
      if (!this.canDraft) {
        this.snackbarText = this.totalCost > this.balance 
          ? 'Insufficient funds to complete this draft' 
          : 'Please enter a valid quantity';
        this.snackbarColor = 'error';
        this.snackbar = true;
        return;
      }

      const totalCost = this.selectedStock.current_price * this.draftQuantity;
      if (totalCost > this.balance) {
        this.snackbarText = 'Insufficient funds to complete this draft';
        this.snackbarColor = 'error';
        this.snackbar = true;
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('/api/stocks/draft/', 
          { 
            symbol: this.selectedStock.symbol,
            quantity: this.draftQuantity
          },
          { 
            headers: { 
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json',
            } 
          }
        );
        console.log('Draft response:', response.data);
        this.snackbarText = `Successfully drafted ${this.draftQuantity} shares of ${this.selectedStock.name}`;
        this.snackbarColor = 'success';
        this.snackbar = true;
        this.balance = response.data.remaining_balance;
        this.closeDraftDialog();
        this.fetchPortfolio(); // Refresh the portfolio
        this.fetchAvailableStocks(); // Refresh the available stocks
      } catch (error) {
        console.error('Error drafting stock:', error.response ? error.response.data : error);
        this.snackbarText = 'Failed to draft stock. Please try again.';
        this.snackbarColor = 'error';
        this.snackbar = true;
      }
    },
    updateTableOptions(options) {
      this.tableOptions = options;
    },
  },
}
</script>

<style scoped>
.draft-title {
  background: linear-gradient(to right, #30CFD0 0%, #330867 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 3rem;
  text-transform: uppercase;
  letter-spacing: 2px;
}
.title-word {
  animation: color-animation 4s linear infinite;
}
.title-word-1 {
  --color-1: #ACCFCB;
  --color-2: #E4A9A8;
  --color-3: #ACCFCB;
}
</style>