<template>
  <v-container fluid class="fill-height pa-0" style="background: linear-gradient(to right, #2196F3, #4CAF50);">
    <v-row align="center" justify="center" class="mx-0">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="12" class="pa-6">
          <v-card-title class="dashboard-title text-h4 font-weight-bold text-center mb-4">
            {{formattedUsername}} Dashboard
          </v-card-title>

          <v-card outlined>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Weekly Portfolio</span>
              <v-btn color="primary" to="/draft">
                <v-icon left>mdi-plus</v-icon>
                Draft Stocks
              </v-btn>
            </v-card-title>
            <v-card-text>
              <v-data-table
                :headers="table_headers"
                :items="portfolioWithTotalValue"
                :options.sync="tableOptions"
                @update:options="updateTableOptions"
                :items-per-page="tableOptions.itemsPerPage"
                :page.sync="tableOptions.page"
                :sort-by="tableOptions.sortBy"
                :sort-desc="tableOptions.sortDesc"
                show-headers
              >
                <template v-slot:item.stock.symbol="{ item }">
                  <v-chip :color="getRandomColor(item.stock.symbol)" text-color="white" small>
                    {{ item.stock.symbol }}
                  </v-chip>
                </template>
                <template v-slot:item.stock.purchase_price="{ item }">
                  ${{ item.stock.purchase_price.toFixed(2) }}
                </template>
                <template v-slot:item.stock.current_price="{ item }">
                  ${{ item.stock.current_price.toFixed(2) }}
                </template>
                <template v-slot:item.totalValue="{ item }">
                  ${{ item.totalValue.toFixed(2) }}
                </template>
                <template v-slot:item.gain_loss="{ item }">
                  <span :class="item.gain_loss >= 0 ? 'success--text' : 'error--text'">
                    {{ item.gain_loss >= 0 ? '+' : '-' }}${{ Math.abs(item.gain_loss).toFixed(2) }}
                  </span>
                </template>
                <template v-slot:item.actions="{ item }">
                  <v-btn small color="success" @click="openBuyDialog(item)" :disabled="item.stock.current_price > availableBalance">Buy</v-btn>
                  <v-btn small color="error" @click="openSellDialog(item)">Sell</v-btn>
                </template>
                <template v-slot:footer>
                  <v-row class="mt-2 pa-2" align="center" justify="space-between">
                    <strong>Total Portfolio Value:</strong>
                    <span :class="['text-h5', totalPortfolioValueColor]">${{ totalPortfolioValue.toFixed(2) }}</span>
                  </v-row>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>

          <v-card outlined class="mt-6">
            <v-card-title>Performance Overview</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <v-card outlined>
                    <v-card-text class="text-center">
                      <div class="text-h6">Total Gain/Loss</div>
                      <div :class="['text-h4', gainLossColor]">
                        {{ totalGainLoss >= 0 ? '+' : '-' }}${{ Math.abs(totalGainLoss).toFixed(2) }}
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-card outlined>
                    <v-card-text class="text-center">
                      <div class="text-h6">Total Portfolio Value</div>
                      <div :class="['text-h4', totalPortfolioValueColor]">${{ totalPortfolioValue.toFixed(2) }}</div>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <v-card outlined>
                    <v-card-text class="text-center">
                      <div class="text-h6">Available Balance</div>
                      <div class="text-h4 primary--text">${{ balance.toFixed(2) }}</div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
          <v-card outlined class="mt-6">
            <v-card-title>Persistent Portfolio</v-card-title>
            <v-card-text>
              <v-data-table
                :headers="persistentPortfolioHeaders"
                :items="persistentPortfolio"
                :options.sync="persistentPortfolioOptions"
                @update:options="options => persistentPortfolioOptions = options"
                :items-per-page="persistentPortfolioOptions.itemsPerPage"
                :page.sync="persistentPortfolioOptions.page"
                :sort-by="persistentPortfolioOptions.sortBy"
                :sort-desc="persistentPortfolioOptions.sortDesc"
                show-headers
                class="persistent-portfolio-table"
              >
                <template v-slot:item="{ item }">
                  <tr :class="getRowClass(item)">
                    <td class="text-center">
                      <v-chip :color="getRandomColor(item.symbol)" text-color="white" small>
                        {{ item.symbol || 'N/A' }}
                      </v-chip>
                    </td>
                    <td class="text-center">{{ item.name }}</td>
                    <td class="text-center">{{ item.tags }}</td>
                    <td class="text-center">{{ item.quantity }}</td>
                    <td class="text-center">${{ item.purchase_price.toFixed(2) }}</td>
                    <td class="text-center">${{ item.current_price.toFixed(2) }}</td>
                    <td class="text-center">₥{{ item.totalValue.toFixed(2) }}</td>
                    <td class="text-center">
                      <span :class="item.gain_loss >= 0 ? 'success--text' : 'error--text'">
                        {{ item.gain_loss >= 0 ? '+' : '-' }}₥{{ Math.abs(item.gain_loss).toFixed(2) }}
                      </span>
                    </td>
                    <td class="text-center">
                      <v-btn small color="success" @click="buyPersistentStock(item)" :disabled="availableGains < item.current_price" class="mr-2">Buy</v-btn>
                      <v-btn small color="error" @click="sellPersistentStock(item)">Sell</v-btn>
                    </td>
                  </tr>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
          <v-card outlined class="mt-6">
            <v-card-title>Persistent Performance Overview</v-card-title>
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6" md="6">
                  <v-card outlined>
                    <v-card-text class="text-center">
                      <div class="text-h6">Available Gains</div>
                      <div :class="['text-h4', availableGainColor]">${{ availableGains.toFixed(2) }}</div>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="6">
                  <v-card outlined>
                    <v-card-text class="text-center">
                      <div class="text-h6">Total Gain/Loss</div>
                      <div :class="['text-h4', persistentGainLossColor]">
                        {{ persistentGainLoss >= 0 ? '+' : '-' }}₥{{ Math.abs(persistentGainLoss).toFixed(2) }}
                      </div>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="6">
                  <v-card outlined>
                    <v-card-text class="text-center">
                      <div class="text-h6">Total Portfolio Value</div>
                      <div :class="['text-h4', persistentTotalValueColor]">₥{{ persistentTotalValue.toFixed(2) }}</div>
                    </v-card-text>
                  </v-card>
                </v-col>
                <v-col cols="12" sm="6" md="6">
                  <v-card outlined>
                    <v-card-text class="text-center">
                      <div class="text-h6">Total MOQs</div>
                      <div class="text-h4">₥{{ availableMoqs }}</div>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-card>
        
      </v-col>
    </v-row>
    <!-- Buy Stock Dialog -->
    <v-dialog v-model="buyDialog" max-width="400px">
      <v-card>
        <v-card-title>Buy Shares</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <p>Stock: {{ selectedStock ? selectedStock.stock.name : '' }}</p>
              <p>Current Price: ${{ selectedStock ? Number(selectedStock.stock.current_price).toFixed(2) : '0.00' }}</p>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model.number="buyQuantity"
                label="Number of Shares"
                type="number"
                min="1"
                :rules="[v => v > 0 || 'Quantity must be greater than 0']"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <p class="font-weight-bold">Total Cost: ${{ totalCost.toFixed(2) }}</p>
              <p :class="{'error--text': totalCost > availableBalance}">
                Remaining Balance: ${{ remainingBalance }}
              </p>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeBuyDialog">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="confirmBuy" :disabled="!canBuy">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Buy Persistent Stock Dialog -->
    <v-dialog v-model="buyPersistentDialog" max-width="400px">
  <v-card v-if="selectedStock">
    <v-card-title>Buy Persistent Stock</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <p>Stock: {{ selectedStock.stock.name }}</p>
          <p>Current Price: ${{ Number(selectedStock.stock.current_price).toFixed(2) }}</p>
        </v-col>
        <v-col cols="12">
          <v-text-field
            v-model.number="buyQuantity"
            label="Number of Shares"
            type="number"
            min="1"
            :rules="[v => v > 0 || 'Quantity must be greater than 0']"
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <p class="font-weight-bold">Total Cost: ${{ (selectedStock.stock.current_price * buyQuantity).toFixed(2) }}</p>
          <p :class="{'error--text': selectedStock.stock.current_price * buyQuantity > availableGains}">
            Remaining Gains: ${{ (availableGains - (selectedStock.stock.current_price * buyQuantity)).toFixed(2) }}
          </p>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="blue darken-1" text @click="buyPersistentDialog = false">Cancel</v-btn>
      <v-btn color="blue darken-1" text @click="confirmBuyPersistent" :disabled="!canBuyPersistent">Confirm</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

    <!-- Sell Persistent Stock Dialog -->
    <v-dialog v-model="sellPersistentDialog" max-width="400px">
  <v-card v-if="selectedStock">
    <v-card-title>Sell Persistent Stock</v-card-title>
    <v-card-text>
      <v-row>
        <v-col cols="12">
          <p>Stock: {{ selectedStock.name }}</p>
          <p>Current Price: ${{ Number(selectedStock.current_price).toFixed(2) }}</p>
          <p>Available Quantity: {{ selectedStock.quantity }}</p>
        </v-col>
        <v-col cols="12">
          <v-text-field
            v-model.number="sellQuantity"
            label="Number of Shares to Sell"
            type="number"
            min="1"
            :max="selectedStock.quantity"
            :rules="[v => v > 0 || 'Quantity must be greater than 0', v => v <= selectedStock.quantity || 'Cannot sell more than you own']"
          ></v-text-field>
        </v-col>
        <v-col cols="12">
          <p class="font-weight-bold">Estimated MOQs to Receive: {{ (selectedStock.stock.current_price * sellQuantity).toFixed(2) }}</p>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="blue darken-1" text @click="sellPersistentDialog = false">Cancel</v-btn>
      <v-btn color="blue darken-1" text @click="confirmSellPersistent" :disabled="!canSellPersistent">Confirm</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>

    <v-dialog v-model="sellDialog" max-width="400px">
      <v-card>
        <v-card-title>Sell Shares</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <p>Stock: {{ selectedStock ? selectedStock.stock.symbol : '' }}</p>
              <p>Current Price: ${{ selectedStock ? selectedStock.stock.current_price : 0 }}</p>
              <p>Owned Shares: {{ selectedStock ? selectedStock.quantity : 0 }}</p>
            </v-col>
            <v-col cols="12">
              <v-text-field
                v-model.number="sellQuantity"
                label="Number of Shares to Sell"
                type="number"
                min="1"
                :max="selectedStock ? selectedStock.quantity : 1"
                :rules="[
                  v => v > 0 || 'Quantity must be greater than 0',
                  v => v <= (selectedStock ? selectedStock.quantity : 0) || 'Cannot sell more shares than owned'
                ]"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="closeSellDialog">Cancel</v-btn>
          <v-btn color="blue darken-1" text @click="confirmSell">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserDashboard',
  data: () => ({  
    portfolio: [],
    balance: 0,
    username: '',
    buyDialog: false,
    available_balance: 0,
    availableBalance: 0,
    persistentTotalValue: 0,
    persistentGainLoss: 0,
    availableMoqs: 0,
    buyQuantity: 1,
    selectedStock: null,
    buyPersistentDialog: false,
    sellPersistentDialog: false,
    available_moqs: 0,
    persistentPortfolio: [],
    initialInvestment: 50000, // Adjust this value as needed
    table_headers: [
      { title: 'Ticker', align: 'start', value: 'stock.symbol', sortable: true },
      { title: 'Name', align: 'start', value: 'stock.name', sortable: true },
      { title: 'Quantity', align: 'end', value: 'quantity', sortable: true },
      { title: 'Purchase Price', align: 'end', value: 'stock.purchase_price', sortable: true },
      { title: 'Current Price', align: 'end', value: 'stock.current_price', sortable: true },
      { title: 'Total Value', align: 'end', value: 'totalValue', sortable: true },
      { title: 'Gain/Loss', align: 'end', value: 'gain_loss', sortable: true },
      { title: 'Actions', align: 'center', value: 'actions', sortable: false },
    ],
    tableOptions: {
      sortBy: ['stock.symbol'],
      sortDesc: [false],
      page: 1,
      itemsPerPage: 10
    },
    sellDialog: false,
    selectedStock: null,
    sellQuantity: 1,
    persistentPortfolio: [],
    persistentPortfolioHeaders: [
      { title: 'Ticker', align: 'start', value: 'symbol', sortable: true },
      { title: 'Name', align: 'start', value: 'name', sortable: true },
      { title: 'Tags', align: 'start', value: 'tags', sortable: true },
      { title: 'Quantity', align: 'end', value: 'quantity', sortable: true },
      { title: 'Purchase Price', align: 'end', value: 'purchase_price', sortable: true },
      { title: 'Current Price', align: 'end', value: 'current_price', sortable: true },
      { title: 'Total Value', align: 'end', value: 'totalValue', sortable: true },
      { title: 'Gain/Loss', align: 'end', value: 'gain_loss', sortable: true },
      { title: 'Actions', align: 'center', value: 'actions', sortable: false },
    ],
    persistentPortfolioOptions: {
      sortBy: ['symbol'],
      sortDesc: [false],
      page: 1,
      itemsPerPage: 10
    },
    persistentTotalValue: 0,
    persistentGainLoss: 0,
    availableMoqs: 0,
    availableGains: 0,
    totalSpent: 0,
  }),
  computed: {
    formattedUsername() {
      // Format the username to capitalize the first letter. Add an 's or an ' if it ends in 's'
      if (this.username.endsWith('s')) {
        return this.username.charAt(0).toUpperCase() + this.username.slice(1) + "'";
      } else {
        return this.username.charAt(0).toUpperCase() + this.username.slice(1) + "'s";
      }
    },
    persistentGainLossColor() {
    return this.availableGains >= 0 ? 'success--text' : 'error--text';
  },
  availableGainColor() {
    return this.availableGains >= 0 ? 'success--text' : 'error--text';
  },
  persistentTotalValueColor() {
    return this.persistentTotalValue >= 0 ? 'success--text' : 'error--text';
  },
  persistentTotalGainLossColor() {
    return this.calculatedTotalGainLoss >= 0 ? 'success--text' : 'error--text';
  },
  totalPortfolioValueColor() {
    return this.totalPortfolioValue >= 0 ? 'success--text' : 'error--text';
  },
    portfolioWithTotalValue() {
      let portfolio = this.portfolio.map(item => {
        const totalValue = Number(item.quantity) * Number(item.stock.current_price);
        const purchaseValue = Number(item.quantity) * Number(item.stock.purchase_price);
        const gain_loss = totalValue - purchaseValue;
        return {
          ...item,
          totalValue,
          gain_loss,
        };
      });

      // Apply sorting
      if (this.tableOptions && this.tableOptions.sortBy && this.tableOptions.sortBy.length) {
        const sortBy = this.tableOptions.sortBy[0];
        const sortDesc = this.tableOptions.sortDesc ? this.tableOptions.sortDesc[0] : false;
        portfolio = portfolio.sort((a, b) => {
          let aValue = this.getNestedValue(a, sortBy);
          let bValue = this.getNestedValue(b, sortBy);
          let comparison = 0;
          if (aValue < bValue) comparison = -1;
          if (aValue > bValue) comparison = 1;
          return sortDesc ? -comparison : comparison;
        });
      }

      return portfolio;
    },
    totalPortfolioValue() {
      const totalValue = this.portfolioWithTotalValue.reduce((sum, item) => {
        // Use full precision for calculation
        return sum + (Number(item.quantity) * Number(item.stock.current_price));
      }, 0);
      console.log('Total Portfolio Value:', totalValue);
      return totalValue;
    },
    totalGainLoss() {
      const gains = this.totalPortfolioValue + (Math.abs(this.balance) - this.initialInvestment);
      return gains;
    },
    calculatedTotalGainLoss() {
      const gains = this.totalPortfolioValue + (Math.abs(this.balance) - this.initialInvestment) - this.totalSpent;
      this.$nextTick(() => {
        this.updateAvailableGains(gains);
      });
    return gains;
    },
    gainLossColor() {
      return this.totalGainLoss > -.01 ? 'green--text' : 'red--text';
    },
    totalCost() {
    if (this.selectedStock && this.buyQuantity > 0) {
      return Number(this.selectedStock.stock.current_price) * this.buyQuantity;
    }
    return 0;
    },
    canBuy() {
      return this.buyQuantity > 0 && this.totalCost <= this.availableBalance;
    },
    remainingBalance() {
      return Number((this.availableBalance - this.totalCost).toFixed(2));
    },
    persistentGainLossColor() {
      return this.persistentGainLoss >= 0 ? 'success--text' : 'error--text';
    },
    canBuyPersistent() {
      return this.buyQuantity > 0 && this.selectedStock && 
            this.selectedStock.stock && 
            this.selectedStock.stock.current_price * this.buyQuantity <= this.totalGainLoss
    },
  canSellPersistent() {
    return this.sellQuantity > 0 && this.selectedStock && 
           this.sellQuantity <= this.selectedStock.quantity;
  }
  },
  mounted() {
    this.fetchPersistentPortfolio();
    this.fetchPortfolio();
    
    console.log('Headers:', this.table_headers);
  },
  methods: {
    async fetchPortfolio() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('/api/portfolio/', {
          headers: {
            'Authorization': `Token ${token}`
          }
        });
        this.portfolio = response.data.stocks.map(stock => ({
          ...stock,
          quantity: Number(stock.quantity),
          stock: {
            ...stock.stock,
            current_price: Number(stock.stock.current_price),
            purchase_price: Number(stock.stock.purchase_price)
          }
        }));
        this.balance = Number(response.data.balance);
        this.availableBalance = this.balance;
        this.username = response.data.user;
        this.totalSpent = Number(response.data.total_spent);
        this.availableGains = Number(response.data.available_gains);
        this.initialInvestment = Number(response.data.initial_investment);
        console.log('Available Gains from fetchPortfolio:', this.availableGains);
        this.$nextTick(() => {
          this.$forceUpdate();
        });
        
        console.log('Portfolio:', this.portfolio);
        console.log('Balance:', this.balance);
        console.log('Total Portfolio Value:', this.totalPortfolioValue);
        console.log('Total Gain/Loss:', this.totalGainLoss);
        // update total gain loss and available gains
        await this.updateAvailableGains(this.calculatedTotalGainLoss);
      } catch (error) {
        console.error('Error fetching portfolio:', error)
      }
    },
    async updateAvailableGains(newGains) {
      try {
          const token = localStorage.getItem('token');
          console.log('Updating available gains:', newGains);
          const response = await axios.post('/api/update-gains/', {
            available_gains: newGains
          }, {
          headers: {
              'Authorization': `Token ${token}`
            } 
          });
          console.log('Available gains updated successfully:', response.data);

          console.log('Available gains updated successfully');
        } catch (error) {
          console.error('Error updating available gains:', error);
        }
    },
    getRandomColor(symbol) {
      if (!symbol) return 'grey'; // Default color if symbol is undefined
      const colors = ['primary', 'secondary', 'accent', 'success', 'info', 'warning'];
      const index = symbol.charCodeAt(0) % colors.length;
      return colors[index];
    },
    openSellDialog(stock) {
      this.selectedStock = stock;
      this.sellQuantity = 1;
      this.sellDialog = true;
    },
    closeSellDialog() {
      this.sellDialog = false;
      this.selectedStock = null;
      this.sellQuantity = 1;
    },
    async confirmSell() {
      if (this.sellQuantity <= 0 || this.sellQuantity > this.selectedStock.quantity) {
        this.$store.commit('setSnackbar', {
          text: 'Please enter a valid quantity',
          color: 'error'
        });
        return;
      }

      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('/api/sell/', // Changed from '/api/stocks/sell/'
          { 
            symbol: this.selectedStock.stock.symbol,
            quantity: this.sellQuantity
          },
          { 
            headers: { 
              'Authorization': `Token ${token}`,
              'Content-Type': 'application/json',
            } 
          }
        );

        this.$store.commit('setSnackbar', {
          text: `Successfully sold ${this.sellQuantity} shares of ${this.selectedStock.stock.symbol}`,
          color: 'success'
        });

        this.closeSellDialog();
        this.fetchPortfolio(); // Refresh the portfolio
      } catch (error) {
        console.error('Error selling stock:', error.response ? error.response.data : error);
        this.$store.commit('setSnackbar', {
          text: 'Failed to sell stock. Please try again.',
          color: 'error'
        });
      }
    },
    updateTableOptions(options) {
      this.tableOptions = options;
    },
    getRowClass(item) {
      if (item.tags.includes('COMMISSION')) return 'commission-row';
      if (item.tags.includes('TENACIOUS')) return 'tenacious-row';
      if (item.tags.includes('SUBSIDIZED')) return 'subsidized-row';
      if (item.tags.includes('INSIDER')) return 'insider-row';
      if (item.tags.includes('GLITCHED')) return 'glitched-row';
      if (item.tags.includes('SHORTSQUEEZE')) return 'shortsqueeze-row';
      return '';
    },
    getNestedValue(obj, path) {
    if (typeof path === 'string') {
      return path.split('.').reduce((prev, curr) => prev && prev[curr], obj);
    } else if (Array.isArray(path)) {
      return path.reduce((prev, curr) => prev && prev[curr], obj);
    } else {
      return obj[path];
    }
  },
  async fetchPersistentPortfolio() {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/persistent-portfolio/', {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      
      console.log('Persistent Portfolio Response:', response.data);

      if (response.data && Array.isArray(response.data.stocks)) {
        this.persistentPortfolio = response.data.stocks.map(item => ({
          symbol: item.symbol,
          name: item.name,
          quantity: Number(item.quantity),
          purchase_price: Number(item.purchase_price),
          current_price: Number(item.current_price),
          totalValue: Number(item.quantity) * Number(item.current_price),
          gain_loss: (Number(item.current_price) - Number(item.purchase_price)) * Number(item.quantity),
          tags: item.tags
        }));
        this.totalSpent = response.data.total_spent;
        this.persistentTotalValue = response.data.total_value;
        this.persistentGainLoss = response.data.gain_loss;
        // Store available_moqs if needed
        this.availableMoqs = response.data.available_moqs;
      } else {
        console.error('Unexpected data structure for persistent portfolio:', response.data);
        this.persistentPortfolio = [];
        this.availableMoqs = 0;
      }

      console.log('Processed Persistent Portfolio:', this.persistentPortfolio);
      console.log('Available MOQs:', this.availableMoqs);
    } catch (error) {
      console.error('Error fetching persistent portfolio:', error);
      this.persistentPortfolio = [];
      this.availableMoqs = 0;
    }
  },
  openBuyDialog(stock) {
    this.selectedStock = stock;
    this.available_balance = this.balance;
    this.buyQuantity = 1;
    this.buyDialog = true;
  },
  closeBuyDialog() {
    this.buyDialog = false;
    this.selectedStock = null;
    this.buyQuantity = 1;
  },
  async confirmBuy() {
    if (!this.canBuy) {
      this.$store.commit('setSnackbar', {
        text: this.totalCost > this.availableBalance 
          ? 'Insufficient funds to complete this purchase' 
          : 'Please enter a valid quantity',
        color: 'error'
      });
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/stocks/draft/', {
        symbol: this.selectedStock.stock.symbol,
        quantity: this.buyQuantity
      }, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      
      this.$store.commit('setSnackbar', {
        text: `Successfully bought ${this.buyQuantity} shares of ${this.selectedStock.stock.name}`,
        color: 'success'
      });
      
      this.closeBuyDialog();
      await this.fetchPortfolio();
      await this.fetchPersistentPortfolio();
      // this.totalGainLoss = response.data.total_gain_loss;
      console.log('Total Gain/Loss:', this.totalGainLoss);
    } catch (error) {
      console.error('Error buying stock:', error);
      this.$store.commit('setSnackbar', {
        text: 'Failed to buy stock. Please try again.',
        color: 'error'
      });
    }
  },
    buyPersistentStock(stock) {
    this.selectedStock = {
      stock: {
        name: stock.name,
        symbol: stock.symbol,
        current_price: stock.current_price
      },
      quantity: stock.quantity
    };
    this.buyQuantity = 1;
    this.buyPersistentDialog = true;
  },
  sellPersistentStock(stock) {
    this.selectedStock = {
      stock: {
        name: stock.name,
        symbol: stock.symbol,
        current_price: stock.current_price
      },
      quantity: stock.quantity
    };
    this.sellQuantity = 1;
    this.sellPersistentDialog = true;
  },
  async confirmBuyPersistent() {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/persistent-portfolio/buy/', {
        symbol: this.selectedStock.stock.symbol,
        quantity: this.buyQuantity
      }, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      this.$store.commit('setSnackbar', {
        text: `Successfully bought ${this.buyQuantity} shares of ${this.selectedStock.stock.name}`,
        color: 'success'
      });
      console.log('Available Gains after buy:', response.data.available_gains);
      this.buyPersistentDialog = false;
      await this.fetchPersistentPortfolio();
      await this.fetchPortfolio();
    } catch (error) {
      console.error('Error buying persistent stock:', error);
      this.$store.commit('setSnackbar', {
        text: 'Failed to buy stock',
        color: 'error'
      });
    }
  },
  async confirmSellPersistent() {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('/api/persistent-portfolio/sell/', {
        symbol: this.selectedStock.stock.symbol,
        quantity: this.sellQuantity
      }, {
        headers: {
          'Authorization': `Token ${token}`
        }
      });
      this.$store.commit('setSnackbar', {
        text: `Successfully sold ${this.sellQuantity} shares of ${this.selectedStock.stock.name}`,
        color: 'success'
      });
      this.sellPersistentDialog = false;
      await this.fetchPersistentPortfolio();
    } catch (error) {
      console.error('Error selling persistent stock:', error);
      this.$store.commit('setSnackbar', {
        text: 'Failed to sell stock',
        color: 'error'
      });
    }
  },
  },
}
</script>

<style scoped>
th {
  background-color: red !important;
  color: white !important;
  font-size: 18px !important;
  padding: 10px !important;
}

.green--text {
  color: #4CAF50 !important;
}

.red--text {
  color: #F44336 !important;
}

.success--text {
  color: #4CAF50 !important;
}

.error--text {
  color: #F44336 !important;
}

.dashboard-title {
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
  .commission-row {
  background-color: #FFA07A !important; /* Light Salmon */
  animation: glitch 0.5s infinite;
}

.tenacious-row {
  background-color: #98FB98 !important; /* Pale Green */
  animation: glitch 0.5s infinite;
}

.subsidized-row {
  background-color: #87CEFA !important; /* Light Sky Blue */
  animation: glitch 0.5s infinite;
}

.insider-row {
  background-color: #DDA0DD !important; /* Plum */
  animation: glitch 0.5s infinite;
}

.glitched-row {
  background-color: #F0E68C !important; /* Khaki */
  animation: glitch 0.5s infinite;
}

.shortsqueeze-row {
  background-color: #FF6347 !important; /* Tomato */
  animation: glitch 0.5s infinite;
}

@keyframes subtle-glitch {
  0% {
    text-shadow: 0.05em 0 0 rgba(255, 0, 0, 0.75),
                -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
                0.025em 0.05em 0 rgba(0, 0, 255, 0.75);
  }
  14% {
    text-shadow: 0.05em 0 0 rgba(255, 0, 0, 0.75),
                -0.05em -0.025em 0 rgba(0, 255, 0, 0.75),
                0.025em 0.05em 0 rgba(0, 0, 255, 0.75);
  }
  15% {
    text-shadow: -0.05em -0.025em 0 rgba(255, 0, 0, 0.75),
                0.025em 0.025em 0 rgba(0, 255, 0, 0.75),
                -0.05em -0.05em 0 rgba(0, 0, 255, 0.75);
  }
  49% {
    text-shadow: -0.05em -0.025em 0 rgba(255, 0, 0, 0.75),
                0.025em 0.025em 0 rgba(0, 255, 0, 0.75),
                -0.05em -0.05em 0 rgba(0, 0, 255, 0.75);
  }
  50% {
    text-shadow: 0.025em 0.05em 0 rgba(255, 0, 0, 0.75),
                0.05em 0 0 rgba(0, 255, 0, 0.75),
                0 -0.05em 0 rgba(0, 0, 255, 0.75);
  }
  99% {
    text-shadow: 0.025em 0.05em 0 rgba(255, 0, 0, 0.75),
                0.05em 0 0 rgba(0, 255, 0, 0.75),
                0 -0.05em 0 rgba(0, 0, 255, 0.75);
  }
  100% {
    text-shadow: -0.025em 0 0 rgba(255, 0, 0, 0.75),
                -0.025em -0.025em 0 rgba(0, 255, 0, 0.75),
                -0.025em -0.05em 0 rgba(0, 0, 255, 0.75);
  }
}

.glitched-row {
  position: relative;
  background-color: rgba(240, 230, 140, 0.3) !important; /* Khaki with transparency */
  animation: subtle-glitch 2.5s infinite;
}

.glitched-row:hover {
  animation: subtle-glitch 0.3s infinite;
}

.persistent-portfolio-table >>> .v-data-table__wrapper > table > tbody > tr > td {
  vertical-align: middle;
}

.persistent-portfolio-table >>> .v-data-table__wrapper > table > thead > tr > th {
  text-align: center !important;
}

.persistent-portfolio-table >>> .v-data-table__wrapper > table > tbody > tr > td:last-child {
  white-space: nowrap;
}
</style>