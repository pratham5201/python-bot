from flask import Flask, jsonify, request
import re
import long_responses as long
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:5000"], headers=["Content-Type"], methods=["GET", "POST"], supports_credentials=True)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses 
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'hii', 'hiii'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response("To create a new user, login to Asset Panda account >> Go to Gear Icon >> User Configuration >> Create new user >> Fill the details >> Hit 'Save and close'", [ 'to', 'new'], required_words=['how', 'user'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response("Caution: AssetPanda does not suggest you to delete any user because if you delete one then all the data linked with the User will be deleted including action history from the Groups hence we suggest you to change the User status to Inactive", ['how', 'to', 'can'] , required_words=['delete', 'user'])
    response("To change user template, login to Asset Panda account >> Go to Gear Icon >> User Configuration >> Click 'Edit User Permission' for user to change the template >> Select the template under 'User Template' dropdown >> Hit 'Save Permissions' on the top right corner.",  ['change', 'to', 'how', 'can'] , required_words=['user', 'template'])
    response("Please find the attached video links on 2 parts on how to create action\nPart 1: https://www.youtube.com/watch?v=MbEULvcvZyM\nPart 2: https://www.youtube.com/watch?v=ssR5IOac7k8", ['to', 'how', 'can'] , required_words=['action', 'create'])
    response("To perform an action, login to Asset Panda account >> Go to the group in which you want to perform the Action >> Open any record >> Click on Action on the top right >> Select Action >> Fill the required details >> Hit 'Save and Close'", ['action', 'to', 'how', 'can'] , required_words=['perform', 'action'])
    response("To perform a group action, login to Asset Panda account >> Go to the group in which you want to perform the Action >> Select the Assets by checkmarking them from the left corner >> Click on 'Actions' on the top right corner >> Click 'Group Action' >> Select Action >> Fill the required details >> Hit 'Save and Close'", ['action', 'to', 'how', 'can', 'group'] , required_words=['group', 'action'])
    response("To check action history, login to Asset Panda account >> Go to the group of which you want to see the Action history >> Select an Asset >> Click on 'Actions' on the left Panel >> Select the Action from the Dropdown for which you want to see the Action History >> Here you can see the action history of an Asset." , ['check', 'to', 'how'] , required_words=['history', 'action','check'])
    response("Asset Panda is an asset tracking and management software that helps businesses keep track of their assets and inventory.", ['is', 'what'] , required_words=['what', 'asset', 'panda'])
    response("Asset Panda offers a variety of features including asset tracking, inventory management, custom reporting, barcode scanning, and mobile access.", ['are', 'what', 'the'] , required_words=['features', 'asset', 'panda'])
    response("Pricing for Asset Panda varies depending on the number of users and features needed. Contact Asset Panda for a custom quote.", ['does', 'how', 'much'] , required_words=['cost', 'asset', 'panda'])
    response("Any business that needs to track and manage assets can benefit from Asset Panda, including those in industries such as healthcare, education, hospitality, and manufacturing.", ['what', 'types', 'can'] , required_words=['benefit', 'businesses', 'asset', 'panda'])
    response("Yes, Asset Panda is designed to be user-friendly and easy to navigate. The mobile app makes it easy to access asset information from anywhere.", ['is', 'can'] , required_words=['easy', 'use', 'asset', 'panda'])

    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing 
# while True:
#     print('Bot: ' + get_response(input('You: ')))

@app.route('/api', methods=['POST'])
def hello():
    data = request.get_json('message')
    message = data['message']
    print(message)
    if message is None:
        return jsonify({'error': 'Please provide a correct parameter.'}), 400
    bot_response = get_response(message)
    return jsonify({'Bot Response': bot_response})

if __name__ == '__main__':
    app.run()