const DISCORD = require ("discord.js");        // Direct dependency (npm install discordjs)
const JSONFILE = require ("jsonfile");
const CONFIG = require ("./wame.config.json"); // Ressource file (holds the bot properties) FIXME: Put error message &co in separate file
const HELP = require ("./wame.help.json");     // Ressource file (holds help messages)

const WAME = new DISCORD.Client ();            // Create the client, starting point of the bot

var id;             // the bot's description
var command;        // the base command received
var args;           // arguments passed with (after) the base command 

function help (msg, args) {
    var mess = `${CONFIG.code_mark}\n`;
    var all = false;
    var comm = "";
    if (args[0]) comm = args[0].toLowerCase ();

    switch (comm) {
        case 'options':
            mess = (`${mess}\nOptions\t:\tping, say, kick, slap`);
            break;
        default:
            all = true;
        case 'usage':
            mess = (`${mess}\nUsage   :\t<Prefix><command> <args>`);
            if (!all) break;
        case 'prefix':
            mess = (`${mess}\nPrefix  :\t${HELP.prefix}`);
            if (!all) break;
        case 'id' :
            mess = (`${mess}\nid\t  :\t${HELP.id}`);
            if (!all) break;
        case 'ping':
            mess = (`${mess}\nping\t:\t${HELP.ping}`);
            if (!all) break;
        case 'say':
            mess = (`${mess}\nSay \t:\t${HELP.say}`);
            if (!all) break;
        case 'kick':
            mess = (`${mess}\nkick\t:\t${HELP.kick}`);
            if (!all) break;
        case 'slap':
            mess = (`${mess}\nslap\t:\t${HELP.slap}`);
            if (!all) break;
        case 'help':
            mess = (`${mess}\nHelp\t:\tShow this help message.`);
            break;
    }   

    msg.channel.send (`${mess}\n${CONFIG.code_mark}`);
}

function markdown (msg, mark) {
    return (`${mark}${msg}${mark}`);
}

function wameId (msg) {
    msg.channel.send (CONFIG.id);
}

function slap (msg, args)  {
    msg.channel.send (`Damn it ${msg.mentions.users.first ()}, ${msg.author} is trying to eat over here!`);
}

function kick (msg, args) {
    let mRole = msg.guild.roles.find ("name", "Gabhself");

    if (msg.member.roles.has (mRole.id)) {
        let kicking = msg.guild.member (msg.mentions.users.first ());
        if(!kicking) {
            msg.reply (markdown (CONFIG.kicked_null, CONFIG.code_mark));
        } else {
            let action = 'kick';
            msg.reply (`${CONFIG.vote} ${action} ${kicking} ${CONFIG.acknowledgement}`);
        }
    } else {
        msg.reply (`${markdown (CONFIG.kick_denied, CONFIG.code_mark)}`);
    }
}

function say (msg, args) {
    let mRole = msg.guild.roles.find ("name", "Gabhself");
    if (msg.mentions.everyone) {
        if (msg.member.roles.has (mRole.id)) {
            msg.channel.send (args.join(" "));
        } else { 
            // That should never happen on a well configured server
            msg.reply ("What!? How did you do that?!");
        }
    } else {
        let mess = args.join(" ").replace(/@/g, '[at]');
        msg.channel.send (mess);
    }
}

WAME.on ('guildCreate', guild => {
        guild.defaultChannel.send (`Hello people of ${guild.name}! I hope ${guild.owner.user.username} isn't won't disapprove this early ping`);
});

// FIXME: Guive Gabhself role
WAME.on ('guildMemberAdd', member => {
    let guild = member.guild;
    guild.defaultChannel.send (`Welcome to the Wame show ${member.user}!`);
});

WAME.on ('ready', () => {
    id = WAME.user.username;
    console.log(`Logged in as ${id}!`);
});

WAME.on ('message', msg => {
    if (msg.author.bot) { return; }
    if (!msg.content.startsWith (CONFIG.prefix)) { 
        if (msg.mentions.users.has (WAME.user.id)) {
            msg.channel.send (`Hello ${msg.author}, how can I help you?`);
        }

        return;
    }
    console.log (`Type: Message Author: ${msg.author.username} ID: ${msg.author.id} Input: ${msg.content}`); // Trace

    command = msg.content.split(" ")[0];     // Extract the base command to execute
    command = command.slice (CONFIG.prefix.length);  // Remove the prefix from the command
    args = msg.content.split (" ").slice(1); // Extract the arguments  

    switch (command) {
        case 'ping':
            msg.reply ("Pong!");
            break;
        case 'id'  :
            wameId (msg);
            break;
        case 'say' :
            say (msg, args);
            break;
        case 'help':
            help (msg, args);
            break;
        case 'kick':
            kick (msg,args);
            break;
        case 'slap':
            slap (msg, args);
            break;
        default:
            help (msg, args);
            break;
    }
});

WAME.login(CONFIG.token);
