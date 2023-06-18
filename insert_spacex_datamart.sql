insert into {{ psg_schema }}.spacex_datamart(mission_name, rocket_name, links_count)
select mission_name, rocket_name,
	sum(case when wikipedia is null then 0 else 1 end +
	    case when video_link is null then 0 else 1 end +
		case when reddit_recovery is null then 0 else 1 end +
		case when reddit_media is null then 0 else 1 end +
		case when reddit_launch is null is null then 0 else 1 end +
		  case when presskit is null is null then 0 else 1 end +
		  case when reddit_campaign is null is null then 0 else 1 end +
		  case when mission_patch_small is null is null then 0 else 1 end +
		  case when mission_patch is null is null then 0 else 1 end +
		  case when article_link is null is null then 0 else 1 end) links_count
from public.missions m
	inner join public.launches l on m.launch_id = l.launch_id
	inner join public.rockets r on l.rocket_id = r.rocket_id
group by mission_name, rocket_name