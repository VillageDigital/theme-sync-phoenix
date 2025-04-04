// 📁 app/utils/firestoreSessionStorage.js

import { Firestore } from "@google-cloud/firestore";
import {
  shopifySessionStorage as shopifyFirestoreSessionStorage,
} from "@shopify/shopify-app-session-storage-firestore";

// 🔥 Create a Firestore client instance
const firestore = new Firestore({
  projectId: process.env.GCLOUD_PROJECT_ID,
  keyFilename: process.env.GCLOUD_SERVICE_ACCOUNT_FILE, // path to JSON service account key
});

// 🧠 Setup Firestore session storage for Shopify
const firestoreSessionStorage = shopifyFirestoreSessionStorage(firestore);

export default firestoreSessionStorage;
