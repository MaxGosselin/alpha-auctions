
from django.core.mail import send_mail
from homepage.models import User

import decimal

AUCTION_POSTED="""

\n
Your auction has been accepted.
\n
Thank you for using Alpha Auctions and good luck!
\n
You can view the status of your auction at http://alpha-auctions.herokuapp.com/accounts/login
\n
\n
Alpha Auctions Team 50.

"""

def transaction_notify(transaction):

    winbid = transaction.t_price
    comp = decimal.Decimal(0.01) * winbid
    auction = transaction.t_auction
    buyer = transaction.t_buyer
    seller = transaction.t_seller
    buyer_text = f"""

    Congratulations Team {buyer.team} you have won an auction for:

    \tAsset Type: {auction.asset_class}
    \n
    \tGrade: {auction.grade}
    \n
    \tRegion: {auction.region}
    \n
    \tQuantity: {auction.region}
    \n
    \tShipping Method: {transaction.shipping}
    \n
    ============
    \n
    \tWinning Bid: {winbid}
    \n
    \tTransaction Value: {winbid * auction.quantity}
    \n
    \tTransaction Fee: ${round(comp,2)} CAD

    \n
    Please contact the seller: *Team {seller.team}* through intopmail or at {seller.email}.
    \n
    The service payment to Team 50 (Alpha Auctions) is due immediately upon receipt of this notice. Service payments are to be made to the home office.
    
    \n\n
    Thank you for doing business with Alpha Auctions! Don't hesitate to reach out for help facilitating the complete execution of this transaction.
    \n
    Team 50
    """

    seller_text = f"""

    Congratulations Team {seller.team} you have sold your auction for:

    \tAsset Type: {auction.asset_class}
    \n
    \tGrade: {auction.grade}
    \n
    \tRegion: {auction.region}
    \n
    \tQuantity: {auction.region}
    \n
    \tBuyers Chosen Shipping Method: {transaction.shipping}
    \n
    ============
    \n
    \tWinning Bid: {winbid}
    \n
    \tTransaction Value: {winbid * auction.quantity}
    \n
    \tTransaction Fee: ${round(comp,2)} CAD

    \n
    The buyer *Team {buyer.team}* through intopmail or at {buyer.email}.
    \n
    The service payment to Team 50 (Alpha Auctions) is due immediately upon receipt of this notice. Service payments are to be made to the home office.
    
    \n\n
    Thank you for doing business with Alpha Auctions! Don't hesitate to reach out for help facilitating the complete execution of this transaction.
    \n
    Team 50
    """

    send_mail('You won an Auction on Alpha!', buyer_text, 'auctioneer@mg.maxgosselin.com', [buyer.email, 'team50@itopsim.com',])
    send_mail('Your Auction has sold!', seller_text, 'auctioneer@mg.maxgosselin.com', [seller.email, 'team50@itopsim.com',])
