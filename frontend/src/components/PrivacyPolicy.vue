<template>
    <v-container fluid class="privacy-policy-container pa-0">
      <v-row align="center" justify="center" class="mx-0">
        <v-col cols="12" md="10" lg="8">
          <v-card elevation="12" class="pa-6 main-card">
            <v-card-title class="text-h4 font-weight-bold text-center mb-4 white--text">
              Privacy Policy
            </v-card-title>
            
            <v-expansion-panels>
              <v-expansion-panel
                v-for="(section, index) in policySections"
                :key="index"
              >
                <v-expansion-panel-header class="title panel-header">
                  {{ section.title }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-card-text class="panel-content" v-html="section.content"></v-card-text>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'PrivacyPolicyPage',
    data() {
      return {
        policySections: [
          {
            title: '1. Introduction',
            content: `
              <p>Welcome to Moq Exchange. We respect your privacy and are committed to protecting your personal data. This privacy policy will inform you about how we look after your personal data when you visit our website and tell you about your privacy rights and how the law protects you.</p>
            `
          },
          {
            title: '2. The Data We Collect About You',
            content: `
              <p>We may collect, use, store and transfer different kinds of personal data about you which we have grouped together as follows:</p>
              <ul>
                <li><strong>Identity Data:</strong> includes username or similar identifier.</li>
                <li><strong>Contact Data:</strong> includes email address.</li>
                <li><strong>Technical Data:</strong> includes internet protocol (IP) address, your login data, browser type and version, time zone setting and location, browser plug-in types and versions, operating system and platform, and other technology on the devices you use to access this website.</li>
                <li><strong>Profile Data:</strong> includes your username and password, purchases or orders made by you, your interests, preferences, feedback and survey responses.</li>
                <li><strong>Usage Data:</strong> includes information about how you use our website, products and services.</li>
                <li><strong>Financial Data:</strong> includes virtual currency balances and transaction history within the game.</li>
              </ul>
            `
          },
          {
          title: '3. How We Use Your Personal Data',
          content: `
            <p>We will only use your personal data when the law allows us to. Most commonly, we will use your personal data in the following circumstances:</p>
            <ul>
              <li>Where we need to perform the contract we are about to enter into or have entered into with you.</li>
              <li>Where it is necessary for our legitimate interests (or those of a third party) and your interests and fundamental rights do not override those interests.</li>
              <li>Where we need to comply with a legal obligation.</li>
            </ul>
          `
        },
        {
          title: '4. Data Security',
          content: `
            <p>We have put in place appropriate security measures to prevent your personal data from being accidentally lost, used or accessed in an unauthorized way, altered or disclosed. In addition, we limit access to your personal data to those employees, agents, contractors and other third parties who have a business need to know.</p>
          `
        },
        {
          title: '5. Data Retention',
          content: `
            <p>We will only retain your personal data for as long as reasonably necessary to fulfil the purposes we collected it for, including for the purposes of satisfying any legal, regulatory, tax, accounting or reporting requirements.</p>
          `
        },
        {
          title: '6. Your Legal Rights',
          content: `
            <p>Under certain circumstances, you have rights under data protection laws in relation to your personal data, including the right to:</p>
            <ul>
              <li>Request access to your personal data</li>
              <li>Request correction of your personal data</li>
              <li>Request erasure of your personal data</li>
              <li>Object to processing of your personal data</li>
              <li>Request restriction of processing your personal data</li>
              <li>Request transfer of your personal data</li>
              <li>Right to withdraw consent</li>
            </ul>
            `
          },
          {
            title: '7. Changes to Our Privacy Policy',
            content: `
              <p>We may update this privacy policy from time to time as necessary. The updated version will be indicated by an updated "Revised" date and the updated version will be effective as soon as it is accessible. If we make material changes to this privacy policy, we will notify you by email (sent to the e-mail address specified in your account) or by means of a prominent notice on our website prior to the change becoming effective.</p>
            `
          },
          {
            title: '8. Third Party Links',
            content: `
              <p>Our website may include links to third-party websites, plug-ins and applications. Clicking on those links or enabling those connections may allow third parties to collect or share data about you. We do not control these third-party websites and are not responsible for their privacy statements.</p>
            `
          },
          {
            title: '9. Contact Us',
            content: `
              <p>If you have any questions about this privacy policy or our privacy practices, please contact us at:</p>
              <p>Email: contact@northatlantic.tech</p>
              <p>Moq Exchange</p>
            `
          }
        ]
      }
    }
  }
  </script>
  
  <style scoped>
  .privacy-policy-container {
    background: linear-gradient(to right, #4CAF50, #2196F3);
    min-height: 100vh;
    padding: 2rem 0;
  }
  
  .main-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
  
  .v-card-title {
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  }
  
  .v-expansion-panels {
    background: transparent;
  }
  
  .v-expansion-panel {
    background: rgba(255, 255, 255, 0.15);
    margin-bottom: 1rem;
    border-radius: 15px;
    overflow: hidden;
    transition: all 0.3s ease;
  }
  
  .v-expansion-panel:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
  }
  
  .panel-header {
    background: linear-gradient(45deg, #3949AB, #1E88E5);
    color: #FFFFFF;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
  }
  
  .panel-content {
    background: linear-gradient(to right, #E8F5E9, #E3F2FD);
    color: #1E1E1E;
    border-top: 2px solid #BBDEFB;
    padding: 20px;
  }
  
  .panel-content p {
    margin-bottom: 15px;
  }
  
  .panel-content ul {
    padding-left: 20px;
  }
  
  .panel-content li {
    margin-bottom: 10px;
  }
  </style>