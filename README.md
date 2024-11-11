### **README**

Author: Zetao Huang  
ID: huan2635  

---

### **Project Overview**

This project implements **Phase I: Simple Message Passing Framework**, a real-time messaging system developed using Python socket programming. The system consists of a server and multiple clients functioning as publishers or subscribers. Publishers send topic-specific messages (`WEATHER` and `NEWS`), while subscribers receive messages in real-time based on their subscriptions. The server efficiently manages message distribution, stores messages for future subscribers, and incorporates robust error handling.

---

### **Features**

#### **Server**
- **Topic Management**: Supports two predefined topics: `WEATHER` and `NEWS`.
- **Concurrent Client Handling**: Manages multiple clients simultaneously using multi-threading.
- **Message Storage**: Stores published messages for future delivery to new subscribers.
- **Real-Time Message Distribution**: Forwards messages from publishers to active subscribers immediately.
- **Error Handling**: Provides clear feedback for invalid commands or message formats.

#### **Publisher**
- Publishes messages to a selected topic (`WEATHER` or `NEWS`).
- Receives acknowledgments for successful operations and error messages for invalid formats or topics.
- Can gracefully disconnect by typing `exit`. However, an error message (`<ERROR: Invalid Message Format>`) may occasionally appear, which does not affect the program's functionality.

#### **Subscriber**
- Subscribes to one or both topics (`WEATHER` and `NEWS`).
- Receives:
  1. **Stored Messages**: Messages published before subscription.
  2. **Real-Time Updates**: Messages published by active publishers.
- Handles concurrent subscriptions (e.g., subscribing to both `WEATHER` and `NEWS`) but may experience slight message display overlap, which does not affect functionality.
- Gracefully disconnects by typing `exit`.

#### **Error Handling**
- Prevents publishing or subscribing to non-existent topics.
- Rejects invalid commands or improperly formatted messages with clear error responses.

---

### **How to Run**

#### **1. Start the Server**
1. Open a terminal.
2. Run the server script:
   ```bash
   python Server.py
   ```
3. The server will start and listen for incoming connections on port `12345`.

#### **2. Start the Client**
1. Open another terminal.
2. Run the client script:
   ```bash
   python Client.py
   ```
3. Choose a role:
   - **Publisher**:
     1. Enter a unique name for the publisher.
     2. Select a topic (`WEATHER` or `NEWS`) to publish messages.
     3. Enter messages to send to the selected topic.
     4. Type `exit` to disconnect from the server (note: a harmless `<ERROR: Invalid Message Format>` may appear).
   - **Subscriber**:
     1. Enter a unique name for the subscriber.
     2. Choose a subscription option:
        - `1`: Subscribe to `WEATHER`.
        - `2`: Subscribe to `NEWS`.
        - `3`: Subscribe to both topics (note: minor message overlap may occur).
     3. Receive:
        - **Stored Messages**: Messages published to the topic(s) before subscription.
        - **Real-Time Updates**: Updates as publishers send new messages.
     4. Type `exit` to gracefully disconnect from the server.
 
---

### **Known Issues**

1. **Publisher Exit Error**:
   - **Current Behavior**: When a publisher disconnects by typing `exit`, an `<ERROR: Invalid Message Format>` is displayed.
   - **Impact**: Does not affect the program's functionality.
   - **Resolution**: Pending improvement in publisher exit handling.

2. **Subscriber Message Overlap**:
   - **Current Behavior**: When subscribing to both `WEATHER` and `NEWS`, message display may appear slightly overlapped.
   - **Impact**: Messages are still correctly received and processed.
   - **Resolution**: Pending adjustment of message display logic for enhanced readability.
