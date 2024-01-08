#  ============================================
#  File Name: fake_db.py
#  Description: To define fake_db data.
#  --------------------------------------------
#  Item Name: Whizhack Master Dashboard
#  Author URL: https://whizhack.in

#  ===========================================

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def support(request):
    support_tarcker = {
         "ticket": "123",
         "newticket": "1000",
         "openticket": "20",
         "complete": "100",
         "series": [99]
        }
    return Response(support_tarcker,status=status.HTTP_200_OK)

@api_view(['GET'])
def count(request):
    agents =  {
    "series": [
      100,
      200,
      100,
      150
    ],
    "agent": "4000",
    "aws_agent": "100",
    "azure_agent": "200",
    "gcp_agent": "100",
    "onprim_agent": "150",
    "aws_value": "10",
    "azure_value": "100",
    "gcp_value": "50",
    "onprim_value": "70"
  }
    return Response(agents,status=status.HTTP_200_OK)

@api_view(['GET'])
def service(request):
    sales =  {
      "years": "234",
      "total": "455",
      "labels": [
        "01-08-2022",
        "02-08-2022",
        "03-08-2022",
        "04-08-2022"
      ],
    "series": [
      10,
      200,
      100,
      150
    ]
  }
    return Response(sales,status=status.HTTP_200_OK)


@api_view(['GET'])
def nsrccount(request):
    nsrc = {"series": [50],"silver_count": "50"}
    return Response(nsrc,status=status.HTTP_200_OK)
   
@api_view(['GET'])
def sessions_by_os(request):
    sessions = {
          "chart_info": [
          {
            "usage": "545",
            "updown": "2"
            },
            {
              "usage": "545",
              "updown": "2"
              },
              {
                "usage": "545",
                "updown": "-2"
                }
                ],
                "series":
                [100,40,50]
              }
    return Response(sessions,status=status.HTTP_200_OK)

@api_view(['GET'])
def customers_count(request):
    customers = {
          "chart_info": [
          {
            "usage": "545",
            "updown": "2"
            },
            {
              "usage": "545",
              "updown": "2"
              },
              {
                "usage": "545",
                "updown": "-2"
                }
                ],
                "series":
                [100,40,50]
              }
    return Response(customers,status=status.HTTP_200_OK)

@api_view(['GET'])
def earnings_count(request):
    earnings = {"series": [40,30,20],"month_earning": "456573.09","last_month": "56465","average":"67"}
    return Response(earnings,status=status.HTTP_200_OK)