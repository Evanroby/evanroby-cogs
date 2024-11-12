# Evanroby Cogs - Installation Guide

This guide will walk you through installing and loading cogs from the **Evanroby-cogs** repository on your Red-Discord Bot.
> [!IMPORTANT]
> For support, you can join the official [`Red Cog Support`](https://discord.gg/GET4DVk) server. You can get help on any cogs and any repos in [`#support_othercogs`](https://discord.com/channels/240154543684321280/240212783503900673).
---

## Prerequisites

Before you begin, ensure that you have the `downloader` module loaded on your Red instance.

```py
[p]load downloader
```

---

## Step 1: Add the `Evanroby-cogs` Repository

To access cogs from my collection, add the repository to your Red instance:

```py
[p]repo add Evanroby-cogs https://github.com/Evanroby/evanroby-cogs/
```

---

## Step 2: Install the Desired Cog(s)

Now that the repository is added, you can install the cog(s) you want:

```py
[p]cog install Evanroby-cogs <CogName>
```

> [!NOTE]  
> Replace `<CogName>` with the exact name of the cog you wish to install.

---

## Step 3: Load the Installed Cog(s)

After installing, load the cog to activate it in your bot:

```py
[p]load CogName
```

> [!NOTE] 
> - Ensure you replace `CogName` with the name of the cog you just installed.
> - `[p]` represents your bot's prefix (e.g., `!`, `?`, or any custom prefix you set).

---

## Additional Information

- For a full list of available cogs, visit the [Evanroby-cogs GitHub repository](https://github.com/Evanroby/evanroby-cogs/).
- If you encounter any issues or need support, feel free to open an issue on GitHub or through the important tab all the way up.
## Special Credits
- Thank you to everyone in the official [red server](https://discord.gg/red) for making me discover red, or guiding me on the other cogs.
