// app/utils/firestoreSessionStorage.js
import { Firestore } from "@google-cloud/firestore";

// This is your custom implementation — no Shopify package needed
const firestore = new Firestore({
  projectId: process.env.GCLOUD_PROJECT_ID,
  keyFilename: process.env.GCLOUD_SERVICE_ACCOUNT_FILE,
});

const firestoreSessionStorage = {
  storeCallback: async (session) => {
    await firestore.collection("shopify_sessions").doc(session.id).set(session);
    return true;
  },
  loadCallback: async (id) => {
    const doc = await firestore.collection("shopify_sessions").doc(id).get();
    return doc.exists ? doc.data() : undefined;
  },
  deleteCallback: async (id) => {
    await firestore.collection("shopify_sessions").doc(id).delete();
    return true;
  },
  deleteSessionsCallback: async (ids) => {
    const batch = firestore.batch();
    ids.forEach((id) =>
      batch.delete(firestore.collection("shopify_sessions").doc(id))
    );
    await batch.commit();
    return true;
  },
  findSessionsByShopCallback: async (shop) => {
    const snapshot = await firestore
      .collection("shopify_sessions")
      .where("shop", "==", shop)
      .get();
    return snapshot.docs.map((doc) => doc.data());
  },
};

export default firestoreSessionStorage;
