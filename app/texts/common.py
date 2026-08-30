WELCOME = """
<b>Welcome, {name}!</b>

Press the <b>Help</b> button to learn how to configure the bot.
"""


HELP = """ <b>Commands</b>

<b>Connect</b> — get your <code>user_id</code> and <code>chat_id</code>.

<b>Run</b> — start the parser.

⚙️ <b>Setup</b>

To configure the bot, press the <b>Connect</b> button or send <code>Connect</code> in the chat.

Select the chat you want to connect. The bot will then send you a message containing your <code>user_id</code> and the ID of the selected chat (<code>chat_id</code>).

Copy these values into the corresponding fields in the <code>.env</code> file located in the project directory.

🔧 <b>Parser Configuration</b>

<b>domains.json</b>

Specify the domains you want to parse. For each domain, configure the following parameters:

• <code>tag</code> — the HTML tag containing the image URL.
• <code>class</code> — the HTML class of the target element. This parameter is optional.
• <code>attribute</code> — the HTML attribute containing the image URL. Use <code>src</code> for an image element or <code>href</code> for a link containing the image.

For example:

<pre>{
    "example.com": {
        "tag": "img",
        "attribute": "src",
        "class": "gallery"
        
    }
}</pre>

<b>page_urls</b>

Add the URLs of the web pages you want to parse. Each URL must be placed on a separate line.

You can optionally specify a hashtag after each URL, separated by a space:

<code>https://example.com/page #tesla</code>

The specified hashtag will be attached to the Telegram message containing the parsed images.

If no hashtag is specified for a URL, the value of <code>DEFAULT_HASHTAG</code> from the <code>.env</code> file will be used instead.

If both the URL and <code>DEFAULT_HASHTAG</code> have no hashtag, no hashtag will be added.

<b>.env</b>

Set <code>DEFAULT_HASHTAG</code> to the default hashtag that will be used for all URLs without an explicitly specified hashtag.

For example:

<code>DEFAULT_HASHTAG=#general</code>

If you do not want to use a default hashtag, leave the value empty.
"""
